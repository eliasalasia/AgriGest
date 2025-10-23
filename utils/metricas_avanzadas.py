# metricas_avanzadas.py
def calcular_metricas_hoteleria(reservas_df, habitaciones_df):
    """Calcular métricas profesionales de hoteleria"""
    
    reservas_confirmadas = reservas_df[reservas_df['estado'] == 'confirmada']
    
    metricas = {
        # Ocupación
        'tasa_ocupacion': (len(reservas_confirmadas) / len(reservas_df)) * 100,
        
        # Revenue Management
        'adr': reservas_confirmadas['precio_total'].mean(),
        'revpar': reservas_confirmadas['precio_total'].sum() / len(habitaciones_df),
        
        # Eficiencia operativa
        'estancia_promedio': reservas_confirmadas['duracion_estancia'].mean(),
        'tasa_cancelacion': (len(reservas_df[reservas_df['estado'] == 'cancelada']) / len(reservas_df)) * 100,
        
        # Rentabilidad por habitación
        'ingreso_por_habitacion': reservas_confirmadas.groupby('habitacion_id')['precio_total'].sum(),
    }
    
    return metricas