import unittest

from .emisiones import calcular_emisiones_carbono


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