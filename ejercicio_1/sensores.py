"""
Ejercicio 1 - Sanitización y Análisis Estadístico de Sensores.

Los microcontroladores de EcoTech Solutions envían lecturas térmicas en un
formato heterogéneo. Este módulo normaliza cada registro individual y genera
un reporte consolidado para la toma de decisiones.
"""

UBICACION_POR_DEFECTO = "Sin asignar"


# ---------------------------------------------------------------------------
# Punto A: Normalización de lecturas
# ---------------------------------------------------------------------------
def limpiar_registro_sensor(registro_raw):
    """
    Normaliza un registro crudo de un sensor.

    Recibe un diccionario "sucio", por ejemplo:
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"}

    y devuelve un NUEVO diccionario estandarizado:
        {"sensor_id": "SENSOR-001", "temperatura": 24.5, "ubicacion": "Planta Norte"}

    Reglas:
        - sensor_id: sin espacios sobrantes y en mayúsculas.
        - temperatura: float, sin sufijos de unidad ("C", "°C", etc.).
        - ubicacion: si falta o está vacía, se usa UBICACION_POR_DEFECTO.

    Lanza ValueError si el registro no tiene ID o si la temperatura
    no se puede convertir a número.
    """
    # 1) Identificador: quitamos espacios a los costados y pasamos a mayúsculas.
    sensor_id = str(registro_raw.get("sensor_id", "")).strip().upper()
    if sensor_id == "":
        raise ValueError("Registro sin sensor_id")

    # 2) Temperatura: nos quedamos solo con dígitos, punto decimal y signo menos.
    #    Así "24.5C", " 24.5 °C" o "24,5c" terminan siendo "24.5".
    valor_original = registro_raw.get("temperatura", "")
    temperatura_texto = ""
    for caracter in str(valor_original).replace(",", "."):
        if caracter.isdigit() or caracter in ".-":
            temperatura_texto += caracter

    try:
        temperatura = float(temperatura_texto)
    except ValueError:
        raise ValueError(
            f"Temperatura inválida en el sensor {sensor_id}: '{valor_original}'"
        )

    # 3) Ubicación: valor por defecto si no vino o vino vacía.
    ubicacion = registro_raw.get("ubicacion")
    if ubicacion is None or str(ubicacion).strip() == "":
        ubicacion = UBICACION_POR_DEFECTO
    else:
        ubicacion = str(ubicacion).strip()

    # Devolvemos un diccionario nuevo: el original no se modifica.
    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion,
    }
    
# ---------------------------------------------------------------------------
# Punto B: Monitoreo y mapeo estadístico
# ---------------------------------------------------------------------------
def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    """
    Analiza una lista de registros ya sanitizados con limpiar_registro_sensor().

    Devuelve una tupla (lista_sensores_alerta, promedio_temperatura):
        - lista_sensores_alerta: IDs de los sensores cuya temperatura
          supera el umbral recibido.
        - promedio_temperatura: promedio térmico global, redondeado a 2 decimales.

    Si la lista está vacía devuelve ([], 0.0) para evitar dividir por cero.
    """
    if not lista_sensores_limpios:
        return [], 0.0

    lista_sensores_alerta = []
    suma_temperaturas = 0.0

    # Recorremos una sola vez: acumulamos la suma y detectamos las alertas.
    for sensor in lista_sensores_limpios:
        suma_temperaturas += sensor["temperatura"]
        if sensor["temperatura"] > umbral_temperatura:
            lista_sensores_alerta.append(sensor["sensor_id"])

    promedio_temperatura = round(suma_temperaturas / len(lista_sensores_limpios), 2)
    return lista_sensores_alerta, promedio_temperatura