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


def obtener_metricas_consumo(registros, factor_emision=FACTOR_EMISION_POR_DEFECTO):
    """
    Procesa un historial de consumos por planta industrial.

    Recibe una lista de registros con el formato:
        {"planta": "Planta Norte", "consumo_kwh": 1200}
    (una misma planta puede aparecer varias veces).

    Devuelve un diccionario con:
        - total_consumo_kwh: consumo sumado de todas las plantas.
        - total_emisiones: emisiones globales en kg de CO2.
        - planta_mayor_consumo: nombre de la planta que más consumió
          (None si no hay registros).
        - detalle_plantas: lista con consumo y emisiones por planta,
          ordenada de mayor a menor consumo.
    """
    # Acumulamos consumo y emisiones por planta en un diccionario.
    acumulado_por_planta = {}
    for registro in registros:
        planta = registro["planta"]
        consumo = registro["consumo_kwh"]
        # Cada registro pasa por la función auditada: si algún consumo es
        # negativo, el ValueError corta el procesamiento.
        emisiones = calcular_emisiones_carbono(consumo, factor_emision)

        if planta not in acumulado_por_planta:
            acumulado_por_planta[planta] = {"consumo_kwh": 0, "emisiones": 0.0}
        acumulado_por_planta[planta]["consumo_kwh"] += consumo
        acumulado_por_planta[planta]["emisiones"] += emisiones

    detalle_plantas = [
        {
            "planta": planta,
            "consumo_kwh": datos["consumo_kwh"],
            "emisiones": round(datos["emisiones"], 2),
        }
        for planta, datos in acumulado_por_planta.items()
    ]
    detalle_plantas.sort(key=lambda fila: fila["consumo_kwh"], reverse=True)

    total_consumo_kwh = sum(fila["consumo_kwh"] for fila in detalle_plantas)
    total_emisiones = round(
        sum(datos["emisiones"] for datos in acumulado_por_planta.values()), 2
    )
    planta_mayor_consumo = detalle_plantas[0]["planta"] if detalle_plantas else None

    return {
        "total_consumo_kwh": total_consumo_kwh,
        "total_emisiones": total_emisiones,
        "planta_mayor_consumo": planta_mayor_consumo,
        "detalle_plantas": detalle_plantas,
    }