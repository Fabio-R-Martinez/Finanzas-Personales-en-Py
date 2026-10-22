    from typing import List, Dict

class TransaccionBase:
    """Clase base que encapsula el comportamiento comun entre Ingresos y Gastos."""
    def __init__(self, id_categoria: int, categoria: str, monto_esperado: float = 0.0, monto_ejecutado: float = 0.0):
        self.id_categoria = id_categoria
        self.categoria = categoria
        self.monto_esperado = float(monto_esperado)
        self.monto_ejecutado = float(monto_ejecutado)

    def calcular_diferencia(self) -> float:
        """Calcula la diferencia bruta: Ejecutado - Esperado."""
        return round(self.monto_ejecutado - self.monto_esperado, 2)

    def porcentaje_ejecucion(self) -> float:
        """Calcula el % ejecutado sobre el presupuesto planificado."""
        if self.monto_esperado == 0:
            return 100.0 if self.monto_ejecutado == 0 else 0.0
        return round((self.monto_ejecutado / self.monto_esperado) * 100.0, 2)


class Ingreso(TransaccionBase):
    """Representa un rubro de ingreso (ej. Sueldo, Trabajos Eventuales)."""
    
    def esta_cumplido(self) -> bool:
        """Retorna True si los ingresos reales alcanzaron o superaron la meta."""
        return self.monto_ejecutado >= self.monto_esperado

    def faltante_por_ingresar(self) -> float:
        """Monto restarle para cumplir con la expectativa de ingreso."""
        return max(0.0, round(self.monto_esperado - self.monto_ejecutado, 2))


class Gasto(TransaccionBase):
    """Representa un rubro de egreso (ej. Alimentacion, Servicios, Transporte)."""

    def esta_excedido(self) -> bool:
        """Retorna True si el gasto real supero el limite planificado."""
        return self.monto_ejecutado > self.monto_esperado

    def monto_excedido(self) -> float:
        """Monto gastado de mas sobre el presupuesto limite."""
        return max(0.0, round(self.monto_ejecutado - self.monto_esperado, 2))

    def ahorro_presupuestario(self) -> float:
        """Monto no gastado dentro del limite presupuestado."""
        return max(0.0, round(self.monto_esperado - self.monto_ejecutado, 2))


class Balance:
    """Consolidador mensual que procesa ingresos y gastos y determina la salud financiera."""
    def __init__(self, periodo: str, ingresos: List[Ingreso] = None, gastos: List[Gasto] = None):
        self.periodo = periodo  # Formato 'YYYY-MM'
        self.ingresos = ingresos if ingresos is not None else []
        self.gastos = gastos if gastos is not None else []

    def agregar_ingreso(self, ingreso: Ingreso):
        self.ingresos.append(ingreso)

    def agregar_gasto(self, gasto: Gasto):
        self.gastos.append(gasto)

    # --- PROPIEDADES DE INGRESOS ---
    @property
    def total_ingresos_esperados(self) -> float:
        return round(sum(i.monto_esperado for i in self.ingresos), 2)

    @property
    def total_ingresos_ejecutados(self) -> float:
        return round(sum(i.monto_ejecutado for i in self.ingresos), 2)

    def desviacion_ingresos(self) -> float:
        """Positivo = Ingreso extra real; Negativo = Ingreso faltante."""
        return round(self.total_ingresos_ejecutados - self.total_ingresos_esperados, 2)

    # --- PROPIEDADES DE GASTOS ---
    @property
    def total_gastos_esperados(self) -> float:
        return round(sum(g.monto_esperado for g in self.gastos), 2)

    @property
    def total_gastos_ejecutados(self) -> float:
        return round(sum(g.monto_ejecutado for g in self.gastos), 2)

    def desviacion_gastos(self) -> float:
        """Positivo = Sobregasto total; Negativo = Ahorro por menor gasto."""
        return round(self.total_gastos_ejecutados - self.total_gastos_esperados, 2)

    # --- BALANCE Y DESVIACION NETO ---
    def balance_esperado(self) -> float:
        """Ahorro/Superávit proyectado en papel."""
        return round(self.total_ingresos_esperados - self.total_gastos_esperados, 2)

    def balance_ejecutado(self) -> float:
        """Ahorro/Superávit real conseguido en el bolsillo."""
        return round(self.total_ingresos_ejecutados - self.total_gastos_ejecutados, 2)

    def desviacion_neto_balance(self) -> float:
        """Diferencia entre el ahorro conseguido y el planificado (Real - Esperado)."""
        return round(self.balance_ejecutado() - self.balance_esperado(), 2)

    def diagnostico_resumen(self) -> str:
        """Diagnostico cualitativo inmediato para el usuario."""
        desviacion = self.desviacion_neto_balance()
        if desviacion > 0:
            return f"SUPERÁVIT SUPERIOR: Lograste ahorrar ${desviacion:.2f} más de lo presupuestado."
        elif desviacion == 0:
            return "CUMPLIMIENTO EXACTO: Tu dinero se ejecutó exactamente según lo planificado."
        else:
            return f"DESVIACIÓN NEGATIVA: Tu ahorro real quedó ${abs(desviacion):.2f} por debajo de la meta."

    def obtener_resumen_dict(self) -> Dict:
        return {
            "periodo": self.periodo,
            "ingresos_esperados": self.total_ingresos_esperados,
            "ingresos_ejecutados": self.total_ingresos_ejecutados,
            "desviacion_ingresos": self.desviacion_ingresos(),
            "gastos_esperados": self.total_gastos_esperados,
            "gastos_ejecutados": self.total_gastos_ejecutados,
            "desviacion_gastos": self.desviacion_gastos(),
            "balance_esperado": self.balance_esperado(),
            "balance_ejecutado": self.balance_ejecutado(),
            "desviacion_neto": self.desviacion_neto_balance(),
            "diagnostico": self.diagnostico_resumen()
        }