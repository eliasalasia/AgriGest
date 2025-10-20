import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuración para reproducibilidad
np.random.seed(42)
random.seed(42)

def generar_clientes(n=200):
    """Generar dataset de clientes realistas"""
    nombres = ['Marco', 'Laura', 'Alessandro', 'Chiara', 'Thomas', 'Sophie', 'Giuseppe', 'Elena', 
               'Robert', 'Anna', 'Luca', 'Maria', 'Francesco', 'Giovanna', 'Stefan', 'Petra']
    apellidos = ['Rossi', 'Bianchi', 'Ferrari', 'Esposito', 'Romano', 'Colombo', 'Ricci', 'Marino',
                 'Weber', 'Müller', 'Schmidt', 'Fischer', 'Dubois', 'Bernard', 'Leroy']
    
    paises = ['Italia', 'Alemania', 'Austria', 'Francia', 'Suiza', 'España', 'Reino Unido', 'EEUU']
    
    clientes = []
    for i in range(1, n + 1):
        nombre = f"{random.choice(nombres)} {random.choice(apellidos)}"
        email = f"{nombre.lower().replace(' ', '.')}@email.com"
        telefono = f"+39 {random.randint(300, 399)}{random.randint(1000000, 9999999)}"
        pais = random.choice(paises)
        
        # Fecha de registro (últimos 2 años)
        fecha_reg = datetime.now() - timedelta(days=random.randint(1, 730))
        
        clientes.append({
            'id': i,
            'nombre': nombre,
            'email': email,
            'telefono': telefono,
            'pais': pais,
            'fecha_registro': fecha_reg.strftime('%Y-%m-%d')
        })
    
    return pd.DataFrame(clientes)

def generar_habitaciones():
    """Generar las habitaciones disponibles"""
    habitaciones = [
        {'id': 1, 'nombre': 'Casa Rural Los Alpes', 'tipo': 'Casa Completa', 'capacidad': 6, 'precio_base': 120},
        {'id': 2, 'nombre': 'Suite Viñedos', 'tipo': 'Suite', 'capacidad': 4, 'precio_base': 90},
        {'id': 3, 'nombre': 'Habitación Olivos', 'tipo': 'Doble', 'capacidad': 2, 'precio_base': 65},
        {'id': 4, 'nombre': 'Loft Montaña', 'tipo': 'Loft', 'capacidad': 3, 'precio_base': 75},
        {'id': 5, 'nombre': 'Cabaña Rustica', 'tipo': 'Cabaña', 'capacidad': 5, 'precio_base': 110},
        {'id': 6, 'nombre': 'Habitación Lago', 'tipo': 'Doble', 'capacidad': 2, 'precio_base': 70},
        {'id': 7, 'nombre': 'Suite Familiar', 'tipo': 'Suite', 'capacidad': 6, 'precio_base': 130},
        {'id': 8, 'nombre': 'Estudio Campo', 'tipo': 'Estudio', 'capacidad': 2, 'precio_base': 60}
    ]
    return pd.DataFrame(habitaciones)

def generar_productos():
    """Generar productos locales típicos de Friuli"""
    productos = [
        {'id': 1, 'nombre': 'Vino Friulano Blanco', 'categoria': 'Bebidas', 'stock': 50, 'precio_compra': 8, 'precio_venta': 15},
        {'id': 2, 'nombre': 'Aceite de Oliva Extra', 'categoria': 'Alimentación', 'stock': 30, 'precio_compra': 12, 'precio_venta': 22},
        {'id': 3, 'nombre': 'Miel de Acacia', 'categoria': 'Alimentación', 'stock': 25, 'precio_compra': 6, 'precio_venta': 12},
        {'id': 4, 'nombre': 'Queso Montasio', 'categoria': 'Alimentación', 'stock': 40, 'precio_compra': 9, 'precio_venta': 18},
        {'id': 5, 'nombre': 'Set de Toallas', 'categoria': 'Amenities', 'stock': 100, 'precio_compra': 15, 'precio_venta': 0},
        {'id': 6, 'nombre': 'Jabón Artesanal', 'categoria': 'Amenities', 'stock': 200, 'precio_compra': 2, 'precio_venta': 0},
        {'id': 7, 'nombre': 'Mermelada de Arándanos', 'categoria': 'Alimentación', 'stock': 35, 'precio_compra': 4, 'precio_venta': 8},
        {'id': 8, 'nombre': 'Grappa', 'categoria': 'Bebidas', 'stock': 20, 'precio_compra': 10, 'precio_venta': 20}
    ]
    return pd.DataFrame(productos)

def generar_reservas(clientes_df, habitaciones_df, n_reservas=300):
    """Generar reservas realistas con estacionalidad"""
    reservas = []
    estados = ['confirmada', 'confirmada', 'confirmada', 'pendiente', 'cancelada']  # Más confirmadas
    
    # Patrón estacional (Friuli: alta temporada verano y navidad)
    def es_alta_temporada(fecha):
        mes = fecha.month
        # Verano (junio-agosto) y Navidad (diciembre)
        return mes in [6, 7, 8, 12]
    
    fecha_base = datetime.now() - timedelta(days=365)
    
    for i in range(1, n_reservas + 1):
        cliente_id = random.randint(1, len(clientes_df))
        habitacion_id = random.randint(1, len(habitaciones_df))
        
        # Fechas de reserva (último año)
        dias_desde_base = random.randint(1, 365)
        fecha_entrada = fecha_base + timedelta(days=dias_desde_base)
        
        # Estancia de 1 a 14 días
        duracion = random.randint(1, 14)
        fecha_salida = fecha_entrada + timedelta(days=duracion)
        
        habitacion = habitaciones_df[habitaciones_df['id'] == habitacion_id].iloc[0]
        precio_base = habitacion['precio_base']
        
        # Ajuste por temporada alta
        if es_alta_temporada(fecha_entrada):
            precio_base = int(precio_base * 1.3)  # +30% en temporada alta
        
        # Precio total con posibles extras
        precio_total = precio_base * duracion
        if random.random() > 0.7:  # 30% de probabilidad de extras
            precio_total += random.randint(20, 100)
        
        estado = random.choice(estados)
        num_huespedes = random.randint(1, habitacion['capacidad'])
        
        reservas.append({
            'id': i,
            'cliente_id': cliente_id,
            'habitacion_id': habitacion_id,
            'fecha_entrada': fecha_entrada.strftime('%Y-%m-%d'),
            'fecha_salida': fecha_salida.strftime('%Y-%m-%d'),
            'estado': estado,
            'precio_total': precio_total,
            'num_huespedes': num_huespedes
        })
    
    return pd.DataFrame(reservas)

def main():
    """Función principal para generar todos los datasets"""
    print("Generando datos simulados para AgriGest...")
    
    # Generar todos los datasets
    clientes_df = generar_clientes()
    habitaciones_df = generar_habitaciones()
    productos_df = generar_productos()
    reservas_df = generar_reservas(clientes_df, habitaciones_df)
    
    # Guardar como CSV
    clientes_df.to_csv('data/clientes.csv', index=False)
    habitaciones_df.to_csv('data/habitaciones.csv', index=False)
    productos_df.to_csv('data/productos.csv', index=False)
    reservas_df.to_csv('data/reservas.csv', index=False)
    
    print("✅ Datos generados exitosamente!")
    print(f"📊 Clientes: {len(clientes_df)} registros")
    print(f"🏠 Habitaciones: {len(habitaciones_df)} tipos")
    print(f"🛍️ Productos: {len(productos_df)} items")
    print(f"📅 Reservas: {len(reservas_df)} reservas")
    print("\nArchivos guardados en la carpeta 'data/'")

if __name__ == "__main__":
    main()