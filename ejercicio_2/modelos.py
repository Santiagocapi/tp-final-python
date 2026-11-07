"""
Ejercicio 2 - Punto A: Dominio del catálogo y reglas de inventario.

Define la jerarquía de productos ecológicos de EcoTech Solutions y la
excepción de negocio que protege el stock contra valores inválidos.
"""


# ---------------------------------------------------------------------------
# Excepción personalizada
# ---------------------------------------------------------------------------
class StockInvalidoError(Exception):
    """Se lanza cuando se intenta asignar un stock que viola las reglas de negocio."""

    def __init__(self, stock_recibido):
        self.stock_recibido = stock_recibido
        super().__init__(
            f"Stock inválido: '{stock_recibido}'. "
            "Debe ser un número entero mayor o igual a 0."
        )


# ---------------------------------------------------------------------------
# Clase base
# ---------------------------------------------------------------------------
class DispositivoEcológico:
    """Producto genérico del catálogo de equipamiento sustentable."""

    def __init__(self, modelo, precio, stock):
        self.modelo = modelo
        self.precio = precio
        # No asignamos self.__stock directamente: pasamos por el setter
        # para que la validación se aplique también al crear el objeto.
        self.set_stock(stock)

    # Getter: única forma de leer el atributo privado desde afuera.
    def get_stock(self):
        return self.__stock

    # Setter: única forma de modificarlo, aplicando la regla de negocio.
    def set_stock(self, nuevo_stock):
        # bool es subclase de int en Python, por eso lo excluimos aparte.
        if isinstance(nuevo_stock, bool) or not isinstance(nuevo_stock, int):
            raise StockInvalidoError(nuevo_stock)
        if nuevo_stock < 0:
            raise StockInvalidoError(nuevo_stock)
        self.__stock = nuevo_stock

    def obtener_ficha_tecnica(self):
        """Ficha comercial básica. Las clases hijas la pueden enriquecer."""
        return (
            f"Modelo: {self.modelo} | Precio: ${self.precio:,.2f} "
            f"| Stock: {self.get_stock()} u."
        )

    def a_diccionario(self):
        """Convierte el objeto a un diccionario serializable (patrón DTO)."""
        return {
            "tipo": type(self).__name__,
            "modelo": self.modelo,
            "precio": self.precio,
            "stock": self.get_stock(),
        }

    def __str__(self):
        return self.obtener_ficha_tecnica()


# ---------------------------------------------------------------------------
# Clase especializada
# ---------------------------------------------------------------------------
class PanelSolar(DispositivoEcológico):
    """Panel solar: agrega la potencia nominal en watts."""

    def __init__(self, modelo, precio, stock, eficiencia_watts):
        # Herencia: el padre se encarga de modelo, precio y stock validado.
        super().__init__(modelo, precio, stock)
        self.eficiencia_watts = eficiencia_watts

    # Polimorfismo: mismo nombre de método, comportamiento personalizado.
    def obtener_ficha_tecnica(self):
        ficha_base = super().obtener_ficha_tecnica()
        return f"[Panel Solar] {ficha_base} | Potencia: {self.eficiencia_watts} W"

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["eficiencia_watts"] = self.eficiencia_watts
        return datos