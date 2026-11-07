"""
Ejercicio 2 - Bloque de prueba.

1. Crea productos válidos del catálogo.
2. Verifica la captura controlada de StockInvalidoError.
3. Muestra el polimorfismo de las fichas técnicas.
4. Exporta los productos válidos a catalogo_ecotech.json.
"""

import os

from gestor_inventario import GestorInventario
from modelos import DispositivoEcológico, PanelSolar, StockInvalidoError

# El JSON se guarda siempre al lado de este script, sin importar desde
# qué carpeta se ejecute el programa.
CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_CATALOGO = os.path.join(CARPETA_ACTUAL, "catalogo_ecotech.json")


if __name__ == "__main__":
    print("=" * 60)
    print("       ECOTECH SOLUTIONS - GESTIÓN DEL CATÁLOGO")
    print("=" * 60)

    # Paso 1: creamos productos válidos.
    catalogo = [
        DispositivoEcológico("Termostato-Smart", 350.0, 15),
        DispositivoEcológico("Medidor-Consumo-WiFi", 120.5, 40),
        PanelSolar("SolarMax-500", 1200.0, 8, 500),
        PanelSolar("SolarPro-750", 1850.0, 3, 750),
    ]
    print(f"\n[OK] {len(catalogo)} productos válidos creados.")

    # Paso 2: intentos de stock erróneo, capturados de forma controlada.
    print("\n--- Validación de reglas de inventario ---")

    # 2.a) Al crear un producto con stock negativo.
    try:
        PanelSolar("Panel-Defectuoso", 900.0, -5, 300)
    except StockInvalidoError as error:
        print(f"[ERROR CAPTURADO] Alta rechazada -> {error}")

    # 2.b) Al modificar el stock de un producto existente.
    termostato = catalogo[0]
    try:
        termostato.set_stock(-10)
    except StockInvalidoError as error:
        print(f"[ERROR CAPTURADO] Actualización rechazada -> {error}")
    finally:
        print(f"           Stock de {termostato.modelo} sin cambios: {termostato.get_stock()}")

    # 2.c) Con un valor que no es un número entero.
    try:
        termostato.set_stock("diez")
    except StockInvalidoError as error:
        print(f"[ERROR CAPTURADO] Tipo inválido -> {error}")

    # 2.d) El atributo privado no se puede leer directamente desde afuera.
    try:
        print(termostato.__stock)
    except AttributeError:
        print("[ENCAPSULAMIENTO] __stock no es accesible desde afuera; se usa get_stock().")

    # Paso 3: polimorfismo -> mismo método, distinta ficha según la clase.
    print("\n--- Fichas técnicas comerciales ---")
    for dispositivo in catalogo:
        print(dispositivo.obtener_ficha_tecnica())

    # Paso 4: exportamos los productos válidos a JSON y verificamos.
    print("\n--- Persistencia ---")
    gestor = GestorInventario()
    try:
        cantidad = gestor.guardar_catalogo_json(catalogo, RUTA_CATALOGO)
    except OSError as error:
        print(f"[ERROR] No se pudo guardar el catálogo: {error}")
    else:
        datos_recuperados = gestor.cargar_catalogo_json(RUTA_CATALOGO)
        print(f"[OK] {cantidad} productos exportados a {os.path.basename(RUTA_CATALOGO)}")
        print(f"[OK] Verificación: {len(datos_recuperados)} productos leídos desde el archivo.")
    print("=" * 60)