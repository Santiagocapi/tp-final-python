import unittest

from django.test import SimpleTestCase
from django.urls import reverse

from .emisiones import calcular_emisiones_carbono, obtener_metricas_consumo

# ---------------------------------------------------------------------------
# Punto A: Auditoría del algoritmo de emisiones
# ---------------------------------------------------------------------------
class TestCalculoEmisiones(unittest.TestCase):
    """Valida la exactitud del cálculo y el manejo de consumos fuera de rango."""

    # --- Casos nominales ---
    def test_calculo_con_factor_por_defecto(self):
        self.assertEqual(calcular_emisiones_carbono(100.0), 40.0)

    def test_calculo_con_factor_personalizado(self):
        self.assertEqual(calcular_emisiones_carbono(250.0, 0.5), 125.0)

    def test_calculo_con_decimales(self):
        # Con floats comparamos con tolerancia para evitar errores de redondeo.
        self.assertAlmostEqual(calcular_emisiones_carbono(123.45), 49.38, places=2)

    def test_calculo_con_consumo_entero(self):
        self.assertEqual(calcular_emisiones_carbono(1200), 480.0)

    # --- Casos límite ---
    def test_consumo_cero_no_genera_emisiones(self):
        self.assertEqual(calcular_emisiones_carbono(0), 0.0)

    # --- Casos fuera de rango ---
    def test_consumo_negativo_lanza_value_error(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-50.0)

    def test_consumo_apenas_negativo_lanza_value_error(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-0.01)

    def test_mensaje_de_error_es_descriptivo(self):
        with self.assertRaisesRegex(ValueError, "negativo"):
            calcular_emisiones_carbono(-1, 0.4)


# ---------------------------------------------------------------------------
# Punto B: Procesamiento de métricas
# ---------------------------------------------------------------------------
class TestMetricasConsumo(unittest.TestCase):
    """Valida la agregación del historial de consumos por planta."""

    def setUp(self):
        self.registros = [
            {"planta": "Norte", "consumo_kwh": 1200},
            {"planta": "Sur", "consumo_kwh": 850},
            {"planta": "Norte", "consumo_kwh": 1400},
        ]

    def test_total_de_emisiones(self):
        metricas = obtener_metricas_consumo(self.registros)
        # (1200 + 850 + 1400) * 0.4 = 1380.0
        self.assertEqual(metricas["total_emisiones"], 1380.0)
        self.assertEqual(metricas["total_consumo_kwh"], 3450)

    def test_planta_de_mayor_consumo_suma_todo_su_historial(self):
        metricas = obtener_metricas_consumo(self.registros)
        self.assertEqual(metricas["planta_mayor_consumo"], "Norte")

    def test_detalle_ordenado_de_mayor_a_menor(self):
        detalle = obtener_metricas_consumo(self.registros)["detalle_plantas"]
        self.assertEqual([fila["planta"] for fila in detalle], ["Norte", "Sur"])
        self.assertEqual(detalle[0]["emisiones"], 1040.0)

    def test_lista_vacia(self):
        metricas = obtener_metricas_consumo([])
        self.assertEqual(metricas["total_emisiones"], 0)
        self.assertIsNone(metricas["planta_mayor_consumo"])
        self.assertEqual(metricas["detalle_plantas"], [])

    def test_registro_negativo_propaga_value_error(self):
        self.registros.append({"planta": "Este", "consumo_kwh": -10})
        with self.assertRaises(ValueError):
            obtener_metricas_consumo(self.registros)


# ---------------------------------------------------------------------------
# Integración web: la vista entrega el contexto a la plantilla
# ---------------------------------------------------------------------------
class TestVistaPanelSustentabilidad(SimpleTestCase):

    def test_panel_responde_y_usa_la_plantilla(self):
        respuesta = self.client.get(reverse("panel_sustentabilidad"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "sustentabilidad/panel.html")

    def test_contexto_con_metricas_calculadas(self):
        respuesta = self.client.get(reverse("panel_sustentabilidad"))
        self.assertEqual(respuesta.context["total_emisiones"], 2516.0)
        self.assertEqual(respuesta.context["planta_mayor_consumo"], "Planta Norte")
        self.assertContains(respuesta, "Planta Norte")