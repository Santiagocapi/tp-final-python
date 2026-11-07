"""
Ejercicio 2 - Punto B: Persistencia y gestión del catálogo.

GestorInventario se encarga de guardar (serializar) y leer (deserializar)
el catálogo de dispositivos en formato JSON.
"""

import json


class GestorInventario:
    """Administra la persistencia del catálogo en disco."""

    def guardar_catalogo_json(self, lista_dispositivos, ruta_archivo):
        """
        Serializa una lista de dispositivos y la guarda en un archivo JSON.

        json.dump() no sabe guardar objetos propios (PanelSolar, etc.), así
        que primero convertimos cada uno a diccionario con a_diccionario().

        Devuelve la cantidad de productos guardados.
        """
        catalogo = [dispositivo.a_diccionario() for dispositivo in lista_dispositivos]

        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(catalogo, archivo, indent=4, ensure_ascii=False)

        return len(catalogo)

    def cargar_catalogo_json(self, ruta_archivo):
        """Lee el archivo JSON y devuelve la lista de diccionarios guardada."""
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)