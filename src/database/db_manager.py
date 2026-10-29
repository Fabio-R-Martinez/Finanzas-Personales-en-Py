# src/database/db_manager.py
import sqlite3
from pathlib import Path


class DBManager:
    """Gestor de conexión y operaciones en la base de datos SQLite para Finanzas Personales."""

    def __init__(self, db_path="finanzas_app.db"):
        self.db_path = str(db_path)
        self.init_db()

    def get_connection(self):
        """Retorna una nueva conexión a la base de datos SQLite."""
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Crea las tablas de egresos e ingresos si no existen."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Tabla de categorías de egresos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categorias_egresos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    monto_presupuestado REAL DEFAULT 0.0
                )
            ''')

            # 2. Tabla de gastos efectuados
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS gastos_efectuados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    categoria TEXT NOT NULL,
                    concepto TEXT NOT NULL,
                    monto REAL NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Carga categoría de egreso por defecto si la tabla está vacía
            cursor.execute("SELECT COUNT(*) FROM categorias_egresos")
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO categorias_egresos (nombre, monto_presupuestado) VALUES ('Miscelánea', 0.0)"
                )

            # 3. Inicializar tablas del módulo de ingresos
            self.init_db_ingresos(cursor)

            conn.commit()

    def init_db_ingresos(self, cursor):
        """Crea las tablas para el módulo de ingresos y asegura la existencia de sus campos."""
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias_ingresos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                monto_presupuestado REAL DEFAULT 0.0
            )
        ''')

        # Migración por si la tabla ya existía sin monto_presupuestado
        try:
            cursor.execute("ALTER TABLE categorias_ingresos ADD COLUMN monto_presupuestado REAL DEFAULT 0.0")
        except sqlite3.OperationalError:
            pass

        # Tabla de transacciones de ingresos registrados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ingresos_registrados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                categoria TEXT NOT NULL,
                subcategoria TEXT,
                concepto TEXT NOT NULL,
                monto REAL NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Carga inicial de las 4 categorías principales de ingresos
        cursor.execute("SELECT COUNT(*) FROM categorias_ingresos")
        if cursor.fetchone()[0] == 0:
            categorias_iniciales = [
                ('Sueldo', 0.0),
                ('Trabajo', 0.0),
                ('Venta', 0.0),
                ('Otro', 0.0)
            ]
            cursor.executemany(
                "INSERT INTO categorias_ingresos (nombre, monto_presupuestado) VALUES (?, ?)",
                categorias_iniciales
            )

    # -------------------------------------------------------------------------
    # MÉTODOS CRUD PARA CATEGORÍAS DE EGRESOS / GASTOS
    # -------------------------------------------------------------------------

    def obtener_categorias_egresos(self):
        """Retorna la lista de categorías de egresos con sus presupuestos."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, monto_presupuestado FROM categorias_egresos ORDER BY id ASC")
            rows = cursor.fetchall()
            return [{"id": r[0], "nombre": r[1], "monto_presupuestado": r[2]} for r in rows]

    def agregar_categoria_egreso(self, nombre, monto_presupuestado):
        """Inserta una nueva categoría presupuestada de egreso."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO categorias_egresos (nombre, monto_presupuestado) VALUES (?, ?)",
                (nombre.strip(), float(monto_presupuestado or 0.0))
            )
            conn.commit()

    def actualizar_categoria_egreso(self, id_cat, nuevo_nombre, nuevo_monto):
        """Actualiza el nombre o el monto presupuestado de una categoría de egreso."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE categorias_egresos SET nombre = ?, monto_presupuestado = ? WHERE id = ?",
                (nuevo_nombre.strip(), float(nuevo_monto or 0.0), id_cat)
            )
            conn.commit()

    def eliminar_categoria_egreso(self, id_cat):
        """Elimina una categoría de egreso por su ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM categorias_egresos WHERE id = ?", (id_cat,))
            conn.commit()

    def registrar_gasto_efectuado(self, categoria, concepto, monto):
        """Registra un nuevo gasto efectuado en SQLite (concepto opcional)."""
        concepto_final = concepto.strip() if concepto and concepto.strip() else f"Gasto {categoria}"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO gastos_efectuados (categoria, concepto, monto) VALUES (?, ?, ?)",
                (categoria.strip(), concepto_final, float(monto or 0.0))
            )
            conn.commit()

    def obtener_gastos_por_categoria(self):
        """Retorna la suma acumulada de gastos agrupados por categoría."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.nombre, COALESCE(SUM(g.monto), 0) AS total_gastado
                FROM categorias_egresos c
                LEFT JOIN gastos_efectuados g ON c.nombre = g.categoria
                GROUP BY c.nombre
                ORDER BY total_gastado DESC
            ''')
            rows = cursor.fetchall()
            return [{"categoria": r[0], "total_gastado": r[1]} for r in rows]

    # -------------------------------------------------------------------------
    # MÉTODOS CRUD PARA CATEGORÍAS DE INGRESOS
    # -------------------------------------------------------------------------

    def obtener_categorias_ingresos(self):
        """Retorna las 4 categorías principales de ingresos con su monto presupuestado/esperado."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, monto_presupuestado FROM categorias_ingresos ORDER BY id ASC")
            rows = cursor.fetchall()
            return [{"id": r[0], "nombre": r[1], "monto_presupuestado": r[2]} for r in rows]

    def actualizar_categoria_ingreso(self, id_cat, nuevo_nombre, nuevo_monto):
        """Actualiza el monto presupuestado/esperado de una categoría de ingreso."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE categorias_ingresos SET nombre = ?, monto_presupuestado = ? WHERE id = ?",
                (nuevo_nombre.strip(), float(nuevo_monto or 0.0), id_cat)
            )
            conn.commit()

    def registrar_ingreso(self, categoria, concepto, monto, subcategoria=None):
        """Inserta una nueva transacción de ingreso en SQLite (concepto opcional)."""
        concepto_final = concepto.strip() if concepto and concepto.strip() else f"Ingreso {categoria}"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO ingresos_registrados (categoria, subcategoria, concepto, monto)
                VALUES (?, ?, ?, ?)
                ''',
                (
                    categoria.strip(),
                    subcategoria.strip() if subcategoria else None,
                    concepto_final,
                    float(monto or 0.0)
                )
            )
            conn.commit()

    def obtener_ingresos_por_categoria(self):
        """Retorna la suma acumulada de ingresos agrupados por categoría."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.nombre, COALESCE(SUM(i.monto), 0) AS total_ingresado
                FROM categorias_ingresos c
                LEFT JOIN ingresos_registrados i ON c.nombre = i.categoria
                GROUP BY c.nombre
                ORDER BY total_ingresado DESC
            ''')
            rows = cursor.fetchall()
            return [{"categoria": r[0], "total_ingresado": r[1]} for r in rows]

    # -------------------------------------------------------------------------
    # MÉTODO DE RESUMEN PARA EL DASHBOARD
    # -------------------------------------------------------------------------

    def obtener_resumen_gastos_dashboard(self):
        """Calcula los totales y porcentajes comparativos para las barras del Dashboard."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Total gastado acumulado
            cursor.execute("SELECT COALESCE(SUM(monto), 0) FROM gastos_efectuados")
            total_gastado = float(cursor.fetchone()[0] or 0.0)

            # 2. Total ingresos acumulados / realizados
            cursor.execute("SELECT COALESCE(SUM(monto), 0) FROM ingresos_registrados")
            total_ingresos = float(cursor.fetchone()[0] or 0.0)

            # 3. Total presupuestado de egresos
            cursor.execute("SELECT COALESCE(SUM(monto_presupuestado), 0) FROM categorias_egresos")
            total_presupuestado = float(cursor.fetchone()[0] or 0.0)

            # 4. Total de ingresos esperados / previstos
            cursor.execute("SELECT COALESCE(SUM(monto_presupuestado), 0) FROM categorias_ingresos")
            total_ingresos_esperados = float(cursor.fetchone()[0] or 0.0)

            presupuesto_al_95 = total_presupuestado * 0.95

            # Porcentaje de gastos ejecutados sobre el 95% del presupuesto de egresos
            if presupuesto_al_95 > 0:
                porcentaje_gastos = (total_gastado / presupuesto_al_95) * 100.0
            else:
                porcentaje_gastos = 0.0

            # Porcentaje de ingresos realizados sobre el total de ingresos esperados
            if total_ingresos_esperados > 0:
                porcentaje_ingresos = (total_ingresos / total_ingresos_esperados) * 100.0
            else:
                porcentaje_ingresos = 0.0

            return {
                "total_gastado": total_gastado,
                "total_ingresos": total_ingresos,
                "total_presupuestado": total_presupuestado,
                "total_ingresos_esperados": total_ingresos_esperados,
                "presupuesto_al_95": presupuesto_al_95,
                "porcentaje_gastos": porcentaje_gastos,
                "porcentaje_ingresos": porcentaje_ingresos
            }