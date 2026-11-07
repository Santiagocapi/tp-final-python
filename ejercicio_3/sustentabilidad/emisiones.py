"""
Lógica de negocio de sustentabilidad de EcoTech Solutions.

Este módulo no depende de Django: son funciones de Python puro, lo que
permite auditarlas con unittest de forma aislada y reutilizarlas desde
las vistas web.
"""

FACTOR_EMISION_POR_DEFECTO = 0.4  # kg de CO2 por cada kWh consumido


def calcular_emisiones_carbono(consumo_kwh, factor_emision=FACTOR_EMISION_POR_DEFECTO):
    """
    Calcula las emisiones de CO2 (en kg) de un consumo eléctrico.

    Lanza ValueError si el consumo es negativo.
    """
    if consumo_kwh < 0:
        raise ValueError("El consumo energético no puede ser negativo.")
    return consumo_kwh * factor_emision