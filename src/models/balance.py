# src/models/balance.py

from typing import List, Dict
from src.models.transaccion import Ingreso, Gasto
from src.utils.formatters import fmt_moneda


class Balance:
    """Consolidador mensual que procesa Ingresos y Gastos para determinar la salud financiera."""

    def __init__(self, periodo: str, ingresos: List[Ingreso] = None, gastos: List[Gasto] = None):
        self.periodo = periodo  # Formato 'YYYY-MM'
        self.ingresos = ingresos if ingresos is not None else []
        self.gastos = gastos if gastos is not None else []

    def agregar_ingreso(self, ingreso: Ingreso):
        """Agrega un objeto Ingreso a la lista del mes."""
        self.ingresos.append(ingreso)

    def agregar_gasto(self, gasto: Gasto):
        """Agrega un objeto Gasto a la lista del mes."""
        self.gastos.append(gasto)

    # --- PROPIEDADES DE INGRESOS ---
    @property
    def total_ingresos_esperados(self) -> int:
        """Suma de las metas de ingresos presupuestadas."""
        return sum(i.monto_esperado for i in self.ingresos)

    @property
    def total_ingresos_ejecutados(self) -> int:
        """Suma de los ingresos reales recibidos."""
        return sum(i.monto_ejecutado for i in self.ingresos)

    def desviacion_ingresos(self) -> int:
        """Diferencia entre lo ingresado real y lo esperado (Real - Esperado)."""
        return self.total_ingresos_ejecutados - self.total_ingresos_esperados

    # --- PROPIEDADES DE GASTOS ---
    @property
    def total_gastos_esperados(self) -> int:
        """Suma del presupuesto límite de gastos."""
        return sum(g.monto_esperado for g in self.gastos)

    @property
    def total_gastos_ejecutados(self) -> int:
        """Suma de las compras/gastos reales efectuados."""
        return sum(g.monto_ejecutado for g in self.gastos)

    def desviacion_gastos(self) -> int:
        """Diferencia entre lo gastado real y el presupuesto límite (Real - Esperado)."""
        return self.total_gastos_ejecutados - self.total_gastos_esperados

    # --- BALANCE Y DESVIACIÓN NETO ---
    def balance_esperado(self) -> int:
        """Ahorro/Superávit proyectado en papel (Ingresos Esperados - Gastos Esperados)."""
        return self.total_ingresos_esperados - self.total_gastos_esperados

    def balance_ejecutado(self) -> int:
        """Ahorro/Superávit real en el bolsillo (Ingresos Reales - Gastos Reales)."""
        return self.total_ingresos_ejecutados - self.total_gastos_ejecutados

    def desviacion_neto_balance(self) -> int:
        """Diferencia entre el ahorro real conseguido y la meta planificada."""
        return self.balance_ejecutado() - self.balance_esperado()

    def diagnostico_resumen(self) -> str:
        """Genera una frase de diagnóstico cualitativo para mostrar en el Dashboard."""
        desviacion = self.desviacion_neto_balance()
        if desviacion > 0:
            return f"SUPERÁVIT SUPERIOR: Ahorraste {fmt_moneda(desviacion)} más de lo planificado."
        elif desviacion == 0:
            return "CUMPLIMIENTO EXACTO: Presupuesto ejecutado al 100% según lo planeado."
        else:
            return f"DESVIACIÓN NEGATIVA: Tu ahorro quedó {fmt_moneda(abs(desviacion))} por debajo de la meta."

    def obtener_resumen_dict(self) -> Dict:
        """Retorna un diccionario estructurado listo para ser consumido por la interfaz gráfica."""
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