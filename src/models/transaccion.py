# src/models/transaccion.py

class TransaccionBase:
    """Clase base que contiene los atributos y métodos comunes entre Gastos e Ingresos."""
    
    def __init__(self, id_categoria: int, categoria: str, monto_esperado: int = 0, monto_ejecutado: int = 0):
        self.id_categoria = id_categoria
        self.categoria = categoria
        self.monto_esperado = int(monto_esperado)
        self.monto_ejecutado = int(monto_ejecutado)

    def calcular_diferencia(self) -> int:
        """Calcula la diferencia bruta: Ejecutado - Esperado."""
        return self.monto_ejecutado - self.monto_esperado

    def porcentaje_ejecucion(self) -> int:
        """Calcula qué porcentaje del presupuesto se ha ejecutado."""
        if self.monto_esperado == 0:
            return 100 if self.monto_ejecutado > 0 else 0
        return int((self.monto_ejecutado / self.monto_esperado) * 100)


class Gasto(TransaccionBase):
    """Representa un rubro o partida de gasto (Alimentación, Alquiler, Servicios, etc.)."""

    def esta_excedido(self) -> bool:
        """Retorna True si el gasto real superó el presupuesto planeado."""
        return self.monto_ejecutado > self.monto_esperado

    def monto_excedido(self) -> int:
        """Devuelve el monto exacto gastado de más (0 si se mantuvo en presupuesto)."""
        return max(0, self.monto_ejecutado - self.monto_esperado)

    def ahorro_presupuestario(self) -> int:
        """Devuelve el dinero presupuestado que NO se llegó a gastar."""
        return max(0, self.monto_esperado - self.monto_ejecutado)


class Ingreso(TransaccionBase):
    """Representa una entrada de dinero (Sueldo, Trabajos eventuales, etc.)."""

    def esta_por_debajo(self) -> bool:
        """Retorna True si el ingreso real cobrado fue menor al esperado."""
        return self.monto_ejecutado < self.monto_esperado

    def monto_faltante(self) -> int:
        """Devuelve cuánto dinero faltó para alcanzar la meta de ingresos."""
        return max(0, self.monto_esperado - self.monto_ejecutado)