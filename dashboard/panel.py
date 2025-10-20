import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Configuración de conexión
engine = create_engine("postgresql+pg8000://postgres:Elias1234@localhost:5432/AgriGest")

st.set_page_config(page_title="AgriGest Dashboard", layout="wide")
st.title("📊 Panel de Gestión - AgriGest")

# --- Cargar datos desde PostgreSQL ---
@st.cache_data
def cargar_datos():
    clientes = pd.read_sql_table('clientes', con=engine)
    reservas = pd.read_sql_table('reservas', con=engine)
    habitaciones = pd.read_sql_table('habitaciones', con=engine)
    productos = pd.read_sql_table('productos', con=engine)
    return clientes, reservas, habitaciones, productos

clientes, reservas, habitaciones, productos = cargar_datos()

# --- Sección 1: Resumen general ---
st.subheader("📁 Resumen de registros")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Clientes", len(clientes))
col2.metric("Reservas", len(reservas))
col3.metric("Habitaciones", len(habitaciones))
col4.metric("Productos", len(productos))

# --- Sección 2: Ocupación mensual ---
st.subheader("📅 Ocupación mensual")
reservas['fecha_entrada'] = pd.to_datetime(reservas['fecha_entrada'])
reservas['mes'] = reservas['fecha_entrada'].dt.month
reservas['año'] = reservas['fecha_entrada'].dt.year
confirmadas = reservas[reservas['estado'] == 'confirmada']
ocupacion = confirmadas.groupby(['año', 'mes']).size()
labels = [f"{pd.to_datetime(f'{a}-{m}-01').strftime('%b %Y')}" for a, m in ocupacion.index]
st.bar_chart(pd.Series(ocupacion.values, index=labels))

# --- Sección 3: Ingresos por habitación ---
st.subheader("💰 Ingresos por habitación")
ingresos = confirmadas.groupby('habitacion_id')['precio_total'].sum().reset_index()
ingresos = ingresos.merge(habitaciones[['id', 'nombre']], left_on='habitacion_id', right_on='id')
st.bar_chart(data=ingresos.set_index('nombre')['precio_total'])

# --- Sección 4: Clientes por país ---
st.subheader("🌍 Distribución de clientes por país")
pais_counts = clientes['pais'].value_counts()
st.pyplot(
    pd.Series(pais_counts.values, index=pais_counts.index).plot.pie(
        autopct='%1.1f%%', figsize=(6, 6), title="Clientes por país", ylabel=""
    ).figure
)