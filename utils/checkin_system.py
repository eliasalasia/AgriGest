# checkin_system.py
import streamlit as st
import qrcode
from io import BytesIO
from datetime import datetime

def generar_qr_checkin(reserva_id, cliente_nombre, habitacion_nombre):
    """Generar QR para check-in automático"""
    data = {
        'reserva_id': reserva_id,
        'cliente': cliente_nombre,
        'habitacion': habitacion_nombre,
        'fecha_checkin': datetime.now().isoformat()
    }
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(str(data))
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    
    return buf.getvalue()

# En tu dashboard principal:
def mostrar_modulo_checkin():
    st.sidebar.title("🏠 Check-In Rápido")
    
    reserva_id = st.sidebar.text_input("ID de Reserva")
    if reserva_id:
        # Buscar reserva
        reserva = reservas[reservas['id'] == int(reserva_id)]
        if not reserva.empty:
            cliente_nombre = clientes[clientes['id'] == reserva.iloc[0]['cliente_id']].iloc[0]['nombre']
            habitacion_nombre = habitaciones[habitaciones['id'] == reserva.iloc[0]['habitacion_id']].iloc[0]['nombre']
            
            st.sidebar.success(f"Reserva encontrada: {cliente_nombre}")
            
            # Generar QR
            qr_image = generar_qr_checkin(reserva_id, cliente_nombre, habitacion_nombre)
            st.sidebar.image(qr_image, caption="QR para Check-In", use_column_width=True)
            
            if st.sidebar.button("Confirmar Check-In"):
                # Actualizar estado en base de datos
                st.sidebar.success("✅ Check-in completado")