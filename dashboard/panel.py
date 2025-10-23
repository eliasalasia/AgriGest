import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sqlalchemy import create_engine
import sys
import os

# Agregar el directorio raíz al path para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config

# --- CONFIGURACIÓN SEGURA ---
engine = create_engine(config.DATABASE_URL)

st.set_page_config(
    page_title="AgriGest Pro", 
    layout="wide", 
    page_icon="🏡",
    initial_sidebar_state="expanded"
)

# --- CARGAR DATOS ---
@st.cache_data(ttl=3600)
def cargar_datos():
    try:
        clientes = pd.read_sql_table('clientes', con=engine)
        reservas = pd.read_sql_table('reservas', con=engine)
        habitaciones = pd.read_sql_table('habitaciones', con=engine)
        productos = pd.read_sql_table('productos', con=engine)
        
        # Procesar fechas
        reservas['fecha_entrada'] = pd.to_datetime(reservas['fecha_entrada'])
        reservas['fecha_salida'] = pd.to_datetime(reservas['fecha_salida'])
        reservas['duracion_estancia'] = (reservas['fecha_salida'] - reservas['fecha_entrada']).dt.days
        
        return clientes, reservas, habitaciones, productos
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- INTERFAZ PRINCIPAL ---
st.title("🏡 AgriGest Pro - Dashboard Empresarial")
st.markdown("---")

# Cargar datos
clientes, reservas, habitaciones, productos = cargar_datos()

if not reservas.empty:
    # --- KPIs PRINCIPALES ---
    st.subheader("📈 Métricas Clave")
    
    reservas_confirmadas = reservas[reservas['estado'] == 'confirmada']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Clientes", len(clientes))
    with col2:
        st.metric("Reservas Confirmadas", len(reservas_confirmadas))
    with col3:
        st.metric("Ingresos Totales", f"€{reservas_confirmadas['precio_total'].sum():,.0f}")
    with col4:
        tasa_ocupacion = (len(reservas_confirmadas) / len(reservas)) * 100
        st.metric("Tasa Ocupación", f"{tasa_ocupacion:.1f}%")

    # --- GRÁFICOS PRINCIPALES ---
    col1, col2 = st.columns(2)
    
    with col1:
        # Ingresos por habitación
        ingresos_habitacion = reservas_confirmadas.groupby('habitacion_id')['precio_total'].sum().reset_index()
        ingresos_habitacion = ingresos_habitacion.merge(habitaciones[['id', 'nombre']], left_on='habitacion_id', right_on='id')
        
        fig_ingresos = px.bar(
            ingresos_habitacion,
            x='nombre',
            y='precio_total',
            title='Ingresos por Habitación',
            color='precio_total'
        )
        st.plotly_chart(fig_ingresos, use_container_width=True)
    
    with col2:
        # Clientes por país
        pais_counts = clientes['pais'].value_counts().head(8)
        fig_paises = px.pie(
            values=pais_counts.values,
            names=pais_counts.index,
            title='Clientes por País'
        )
        st.plotly_chart(fig_paises, use_container_width=True)

    # --- OCUPACIÓN MENSUAL ---
    st.subheader("📅 Ocupación Mensual")
    
    reservas_confirmadas['mes'] = reservas_confirmadas['fecha_entrada'].dt.month
    reservas_confirmadas['año'] = reservas_confirmadas['fecha_entrada'].dt.year
    
    ocupacion_mensual = reservas_confirmadas.groupby(['año', 'mes']).size()
    
    if not ocupacion_mensual.empty:
        labels = [f"{m}/{a}" for a, m in ocupacion_mensual.index]
        st.bar_chart(pd.Series(ocupacion_mensual.values, index=labels))

    # --- ALERTAS ---
    st.subheader("🚨 Alertas del Sistema")
    
    # Stock bajo
    stock_bajo = productos[productos['stock'] < 10]
    if not stock_bajo.empty:
        st.warning(f"⚠️ Stock bajo en {len(stock_bajo)} productos")
        for _, prod in stock_bajo.iterrows():
            st.write(f"• {prod['nombre']}: {prod['stock']} unidades")

    # Reservas pendientes
    reservas_pendientes = reservas[reservas['estado'] == 'pendiente']
    if not reservas_pendientes.empty:
        st.info(f"📋 {len(reservas_pendientes)} reservas pendientes de confirmación")

else:
    st.warning("No hay datos de reservas. Ejecuta el simulador de datos primero.")

# --- CHECK-IN RÁPIDO EN SIDEBAR ---
st.sidebar.title("🏠 Check-In Rápido")
reserva_id = st.sidebar.text_input("ID de Reserva")
if reserva_id:
    try:
        reserva = reservas[reservas['id'] == int(reserva_id)]
        if not reserva.empty:
            cliente = clientes[clientes['id'] == reserva.iloc[0]['cliente_id']].iloc[0]
            habitacion = habitaciones[habitaciones['id'] == reserva.iloc[0]['habitacion_id']].iloc[0]
            
            st.sidebar.success(f"Cliente: {cliente['nombre']}")
            st.sidebar.info(f"Habitación: {habitacion['nombre']}")
            
            if st.sidebar.button("Confirmar Check-In"):
                st.sidebar.success("✅ Check-in completado!")
        else:
            st.sidebar.error("Reserva no encontrada")
    except ValueError:
        st.sidebar.error("ID debe ser numérico")