from sqlalchemy import create_engine, text

# Configuración
usuario = 'postgres'
contraseña = 'Elias1234'
host = 'localhost'
puerto = '5432'
base = 'AgriGest'

engine = create_engine(f'postgresql+pg8000://{usuario}:{contraseña}@{host}:{puerto}/{base}')

tablas = ['clientes', 'habitaciones', 'productos', 'reservas']

with engine.connect() as conn:
    for tabla in tablas:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {tabla}"))
        cantidad = result.scalar()
        print(f"📊 Tabla '{tabla}': {cantidad} registros")