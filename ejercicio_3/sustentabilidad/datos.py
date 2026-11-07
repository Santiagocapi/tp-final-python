"""
Historial de consumos que alimenta el panel.

Simula los datos que llegarían desde la tubería de datos de la empresa
(una base de datos, un archivo o una API de los medidores).
"""

REGISTROS_CONSUMO = [
    {"planta": "Planta Norte", "consumo_kwh": 1200},
    {"planta": "Planta Sur", "consumo_kwh": 850},
    {"planta": "Planta Norte", "consumo_kwh": 1400},
    {"planta": "Planta Este", "consumo_kwh": 980},
    {"planta": "Planta Sur", "consumo_kwh": 1100},
    {"planta": "Planta Este", "consumo_kwh": 760},
]