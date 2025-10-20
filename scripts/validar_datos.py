import pandas as pd
import os

def validar_datos():
    """Validar la calidad y consistencia de los datos generados"""
    print("🔍 Validando calidad de datos...")
    
    try:
        # Cargar datasets
        clientes = pd.read_csv('../data/clientes.csv')
        habitaciones = pd.read_csv('../data/habitaciones.csv')
        productos = pd.read_csv('../data/productos.csv')
        reservas = pd.read_csv('../data/reservas.csv')
        
        # Validaciones básicas
        print(f"✅ Clientes: {len(clientes)} registros")
        print(f"✅ Habitaciones: {len(habitaciones)} tipos")
        print(f"✅ Productos: {len(productos)} items")
        print(f"✅ Reservas: {len(reservas)} reservas")
        
        # Validar integridad referencial
        clientes_reservas = reservas['cliente_id'].isin(clientes['id']).all()
        habitaciones_reservas = reservas['habitacion_id'].isin(habitaciones['id']).all()
        
        print(f"🔗 Integridad clientes-reservas: {'✅ OK' if clientes_reservas else '❌ ERROR'}")
        print(f"🔗 Integridad habitaciones-reservas: {'✅ OK' if habitaciones_reservas else '❌ ERROR'}")
        
        # Estadísticas básicas
        print(f"\n📈 Estadísticas de Reservas:")
        print(f"   - Reservas confirmadas: {len(reservas[reservas['estado'] == 'confirmada'])}")
        print(f"   - Reservas pendientes: {len(reservas[reservas['estado'] == 'pendiente'])}")
        print(f"   - Reservas canceladas: {len(reservas[reservas['estado'] == 'cancelada'])}")
        print(f"   - Ingreso total: €{reservas['precio_total'].sum():,.2f}")
        print(f"   - Precio promedio por reserva: €{reservas['precio_total'].mean():.2f}")
        
        # Validar fechas
        reservas['fecha_entrada'] = pd.to_datetime(reservas['fecha_entrada'])
        reservas['fecha_salida'] = pd.to_datetime(reservas['fecha_salida'])
        
        fechas_validas = (reservas['fecha_salida'] > reservas['fecha_entrada']).all()
        print(f"📅 Fechas válidas: {'✅ OK' if fechas_validas else '❌ ERROR'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en validación: {e}")
        return False

if __name__ == "__main__":
    validar_datos()