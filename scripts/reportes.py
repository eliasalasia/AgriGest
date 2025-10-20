import pandas as pd

# Cargar datos
reservas = pd.read_csv('data/reservas.csv')
habitaciones = pd.read_csv('data/habitaciones.csv')

# Convertir fechas
reservas['fecha_entrada'] = pd.to_datetime(reservas['fecha_entrada'])
reservas['mes'] = reservas['fecha_entrada'].dt.month
reservas['año'] = reservas['fecha_entrada'].dt.year

# Ocupación mensual (solo confirmadas)
ocupacion = reservas[reservas['estado'] == 'confirmada'].groupby(['año', 'mes']).size()

# Ingresos por habitación
ingresos = reservas.groupby('habitacion_id')['precio_total'].sum().reset_index()
ingresos = ingresos.merge(habitaciones[['id', 'nombre']], left_on='habitacion_id', right_on='id')

# Mostrar resultados
print("📊 Ocupación mensual:")
print(ocupacion)

print("\n💰 Ingresos por habitación:")
print(ingresos[['nombre', 'precio_total']])