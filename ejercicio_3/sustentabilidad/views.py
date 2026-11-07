from django.shortcuts import render

from .datos import REGISTROS_CONSUMO
from .emisiones import FACTOR_EMISION_POR_DEFECTO, obtener_metricas_consumo


def vista_panel_sustentabilidad(request):
    """Procesa el historial de consumos y renderiza el panel de sustentabilidad."""
    metricas = obtener_metricas_consumo(REGISTROS_CONSUMO)

    contexto = {
        "titulo": "Panel de Sustentabilidad",
        "factor_emision": FACTOR_EMISION_POR_DEFECTO,
        "cantidad_registros": len(REGISTROS_CONSUMO),
        "total_consumo_kwh": metricas["total_consumo_kwh"],
        "total_emisiones": metricas["total_emisiones"],
        "planta_mayor_consumo": metricas["planta_mayor_consumo"],
        "detalle_plantas": metricas["detalle_plantas"],
    }
    return render(request, "sustentabilidad/panel.html", contexto)