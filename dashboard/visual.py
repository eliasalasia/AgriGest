import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
reservas = pd.read_csv('data/reservas.csv')
reservas['fecha_entrada'] = pd.to_datetime(reservas['fecha_entrada'])
reservas['mes'] = reservas['fecha_entrada'].dt.month
reservas['año'] = reservas['fecha_entrada'].dt.year

# Filtrar confirmadas
confirmadas = reservas[reservas['estado'] == 'confirmada']

# Agrupar ingresos por mes
ingresos_mensuales = confirmadas.groupby(['año', 'mes'])['precio_total'].sum().sort_index()

# Crear etiquetas tipo "Oct 2024", "Nov 2024", etc.
labels = [f"{pd.to_datetime(f'{a}-{m}-01').strftime('%b %Y')}" for a, m in ingresos_mensuales.index]

# Visualizar
plt.figure(figsize=(12, 6))
bars = plt.bar(labels, ingresos_mensuales.values, color='#4CAF50', edgecolor='black')

# Añadir valores encima de cada barra
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 200, f"€{int(yval):,}", ha='center', va='bottom', fontsize=9)

plt.title("💰 Ingresos mensuales por reservas confirmadas", fontsize=14, fontweight='bold')
plt.xlabel("Mes", fontsize=12)
plt.ylabel("Ingresos (€)", fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()