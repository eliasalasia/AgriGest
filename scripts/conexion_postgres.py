import pandas as pd
from sqlalchemy import create_engine, text

# Configuración
usuario = 'postgres'
contraseña = 'Elias1234'
host = 'localhost'
puerto = '5432'
base = 'AgriGest'

engine = create_engine(f'postgresql+pg8000://{usuario}:{contraseña}@{host}:{puerto}/{base}')

# Cargar CSVs
clientes = pd.read_csv('data/clientes.csv')
habitaciones = pd.read_csv('data/habitaciones.csv')
productos = pd.read_csv('data/productos.csv')
reservas = pd.read_csv('data/reservas.csv')

# Subir a PostgreSQL
clientes.to_sql('clientes', engine, if_exists='replace', index=False)
habitaciones.to_sql('habitaciones', engine, if_exists='replace', index=False)
productos.to_sql('productos', engine, if_exists='replace', index=False)
reservas.to_sql('reservas', engine, if_exists='replace', index=False)

print("✅ Datos cargados en PostgreSQL")