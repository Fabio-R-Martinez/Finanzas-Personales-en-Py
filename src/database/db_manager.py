# src/database/db_manager.py

import sqlite3
from typing import List
from src.models.transaccion import Gasto, Ingreso
from src.models.balance import Balance


class DBManager:
    """Administrador de persistencia de datos local con SQLite."""

    def __init__(self, db_path: str = "finanzas_app.db"):
        self.db_path = db_path
        self._inicializar_tablas()

    def get_connection(self) -> sqlite3.Connection:
        """Abre y retorna una conexión a la base de datos con claves foráneas activas."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _inicializar_tablas(self):
        """Crea las tablas de categorías, presupuestos y transacciones si no existen."""
        ddl_script = """
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            tipo TEXT CHECK(tipo IN ('INGRESO', 'GASTO')) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS presupuestos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            periodo TEXT NOT NULL,
            categoria_id INTEGER NOT NULL,
            monto_esperado INTEGER NOT NULL CHECK(monto_esperado >= 0),
            FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE,
            UNIQUE(periodo, categoria_id)
        );

        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria_id INTEGER NOT NULL,
            monto_ejecutado INTEGER NOT NULL CHECK(monto_ejecutado >= 0),
            fecha TEXT NOT NULL,
            notas TEXT,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE
        );
        """
        with self.get_connection() as conn:
            conn.executescript(ddl_script)

    # --- OPERACIONES DE CATEGORÍAS ---

    def obtener_categorias(self, tipo: str = "GASTO") -> List[dict]:
        """Obtiene la lista de categorías registradas por tipo ('GASTO' o 'INGRESO')."""
        query = "SELECT id, nombre, tipo FROM categorias WHERE tipo = ? ORDER BY nombre ASC;"
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, (tipo,))
            rows = cur.fetchall()
            return [{"id": r[0], "nombre": r[1], "tipo": r[2]} for r in rows]

    def agregar_categoria(self, nombre: str, tipo: str = "GASTO") -> int:
        """Inserta una nueva categoría si no existe previamente."""
        query = "INSERT OR IGNORE INTO categorias (nombre, tipo) VALUES (?, ?);"
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, (nombre, tipo))
            conn.commit()
            return cur.lastrowid

    # --- OPERACIONES DE PRESUPUESTOS Y GASTOS ---

    def guardar_presupuesto(self, periodo: str, categoria_id: int, monto_esperado: int):
        """Establece o actualiza el monto límite presupuestado para una categoría en un período (YYYY-MM)."""
        query = """
        INSERT INTO presupuestos (periodo, categoria_id, monto_esperado)
        VALUES (?, ?, ?)
        ON CONFLICT(periodo, categoria_id) DO UPDATE SET monto_esperado = excluded.monto_esperado;
        """
        with self.get_connection() as conn:
            conn.execute(query, (periodo, categoria_id, int(monto_esperado)))
            conn.commit()

    def registrar_transaccion(self, categoria_id: int, monto_ejecutado: int, fecha: str, notas: str = ""):
        """Registra un movimiento real ejecutado (compra o pago de gasto)."""
        query = """
        INSERT INTO transacciones (categoria_id, monto_ejecutado, fecha, notas)
        VALUES (?, ?, ?, ?);
        """
        with self.get_connection() as conn:
            conn.execute(query, (categoria_id, int(monto_ejecutado), fecha, notas))
            conn.commit()

    # --- CONSULTAS CONSOLIDADAS (CONEXIÓN CON CAPA POO) ---

    def obtener_gastos_mes(self, periodo: str) -> List[Gasto]:
        """
        Consulta la base de datos para el período especificado ('YYYY-MM') y retorna 
        una lista de objetos 'Gasto' con la suma esperada vs. ejecutada por categoría.
        """
        query = """
        WITH 
        P AS (
            SELECT categoria_id, SUM(monto_esperado) AS total_esperado
            FROM presupuestos WHERE periodo = ? GROUP BY categoria_id
        ),
        T AS (
            SELECT categoria_id, SUM(monto_ejecutado) AS total_ejecutado
            FROM transacciones WHERE strftime('%Y-%m', fecha) = ? GROUP BY categoria_id
        )
        SELECT 
            c.id, 
            c.nombre, 
            COALESCE(P.total_esperado, 0) AS esperado, 
            COALESCE(T.total_ejecutado, 0) AS ejecutado
        FROM categorias c
        LEFT JOIN P ON c.id = P.categoria_id
        LEFT JOIN T ON c.id = T.categoria_id
        WHERE c.tipo = 'GASTO' AND (P.categoria_id IS NOT NULL OR T.categoria_id IS NOT NULL)
        ORDER BY c.nombre ASC;
        """
        gastos = []
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, (periodo, periodo))
            for cat_id, cat_nom, esp, ejec in cur.fetchall():
                gastos.append(Gasto(cat_id, cat_nom, esp, ejec))
        return gastos

    def obtener_balance_mes(self, periodo: str) -> Balance:
        """Genera el objeto Balance consolidado del mes con Ingresos y Gastos."""
        query = """
        WITH 
        P AS (
            SELECT categoria_id, SUM(monto_esperado) AS total_esperado
            FROM presupuestos WHERE periodo = ? GROUP BY categoria_id
        ),
        T AS (
            SELECT categoria_id, SUM(monto_ejecutado) AS total_ejecutado
            FROM transacciones WHERE strftime('%Y-%m', fecha) = ? GROUP BY categoria_id
        )
        SELECT 
            c.id, 
            c.nombre, 
            c.tipo, 
            COALESCE(P.total_esperado, 0), 
            COALESCE(T.total_ejecutado, 0)
        FROM categorias c
        LEFT JOIN P ON c.id = P.categoria_id
        LEFT JOIN T ON c.id = T.categoria_id
        WHERE P.categoria_id IS NOT NULL OR T.categoria_id IS NOT NULL
        ORDER BY c.tipo DESC, c.nombre ASC;
        """
        ingresos, gastos = [], []
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, (periodo, periodo))
            for cat_id, cat_nom, tipo, esp, ejec in cur.fetchall():
                if tipo == 'INGRESO':
                    ingresos.append(Ingreso(cat_id, cat_nom, esp, ejec))
                else:
                    gastos.append(Gasto(cat_id, cat_nom, esp, ejec))
        return Balance(periodo, ingresos, gastos)

    # --- DATOS DE PRUEBA / SEMILLA ---

    def seed_demo_data(self, periodo: str = "2026-09"):
        """Inserta categorías y transacciones de prueba si la base de datos está vacía."""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM categorias;")
            if cur.fetchone()[0] > 0:
                return  # Ya existen datos

        # Categorías
        cat_alim = self.agregar_categoria("Alimentación y Hogar", "GASTO")
        cat_serv = self.agregar_categoria("Servicios y Luz/Gas", "GASTO")
        cat_alq = self.agregar_categoria("Alquiler Vivienda", "GASTO")
        cat_trans = self.agregar_categoria("Transporte y Nafta", "GASTO")
        cat_sueldo = self.agregar_categoria("Sueldo Principal", "INGRESO")
        cat_eventual = self.agregar_categoria("Trabajos Eventuales", "INGRESO")

        # Presupuestos
        self.guardar_presupuesto(periodo, cat_alim, 800000)
        self.guardar_presupuesto(periodo, cat_serv, 250000)
        self.guardar_presupuesto(periodo, cat_alq, 500000)
        self.guardar_presupuesto(periodo, cat_trans, 150000)
        self.guardar_presupuesto(periodo, cat_sueldo, 1500000)
        self.guardar_presupuesto(periodo, cat_eventual, 300000)

        # Transacciones de Gastos
        self.registrar_transaccion(cat_alim, 850000, f"{periodo}-10", "Supermercado")
        self.registrar_transaccion(cat_serv, 260000, f"{periodo}-12", "Pago de facturas")
        self.registrar_transaccion(cat_trans, 120000, f"{periodo}-15", "Carga de combustible")

        # Transacciones de Ingresos
        self.registrar_transaccion(cat_sueldo, 1500000, f"{periodo}-01", "Cobro mensual")
        self.registrar_transaccion(cat_eventual, 200000, f"{periodo}-18", "Trabajo de pintura")