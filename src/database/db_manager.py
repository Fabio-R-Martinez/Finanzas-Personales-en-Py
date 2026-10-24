# src/database/db_manager.py
import sqlite3


class DBManager:
    """Gestor de la base de datos SQLite para Finanzas Personales."""

    def __init__(self, db_path="finanzas_app.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Crea las tablas de categorías y gastos ejecutados si no existen."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Tabla de categorías presupuestadas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categorias_egresos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    monto_presupuestado REAL DEFAULT 0.0
                )
            ''')

            # Tabla de transacciones de gastos efectuados
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS gastos_efectuados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    categoria TEXT NOT NULL,
                    concepto TEXT NOT NULL,
                    monto REAL NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Categoría inicial por defecto
            cursor.execute("SELECT COUNT(*) FROM categorias_egresos")
            if cursor.fetchone()[0] == 0:
                cursor.execute(
                    "INSERT INTO categorias_egresos (nombre, monto_presupuestado) VALUES ('Miscelánea', 0.0)"
                )

            conn.commit()

    def obtener_categorias_egresos(self):
        """Retorna la lista de categorías con sus presupuestos."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nombre, monto_presupuestado FROM categorias_egresos ORDER BY id ASC"
            )
            rows = cursor.fetchall()
            return [
                {"id": r[0], "nombre": r[1], "monto_presupuestado": r[2]}
                for r in rows
            ]

    def agregar_categoria_egreso(self, nombre, monto_presupuestado):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO categorias_egresos (nombre, monto_presupuestado) VALUES (?, ?)",
                (nombre.strip(), float(monto_presupuestado or 0.0)),
            )
            conn.commit()

    def actualizar_categoria_egreso(self, id_cat, nuevo_nombre, nuevo_monto):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE categorias_egresos SET nombre = ?, monto_presupuestado = ? WHERE id = ?",
                (nuevo_nombre.strip(), float(nuevo_monto or 0.0), id_cat),
            )
            conn.commit()

    def eliminar_categoria_egreso(self, id_cat):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM categorias_egresos WHERE id = ?", (id_cat,)
            )
            conn.commit()

    def registrar_gasto_efectuado(self, categoria, concepto, monto):
        """Registra la transacción del gasto ejecutado en la base de datos."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO gastos_efectuados (categoria, concepto, monto) VALUES (?, ?, ?)",
                (categoria.strip(), concepto.strip(), float(monto or 0.0)),
            )
            conn.commit()

    def obtener_total_gastos(self):
        """Calcula el total acumulado de gastos efectuados."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT COALESCE(SUM(monto), 0) FROM gastos_efectuados"
            )
            return cursor.fetchone()[0]

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
    def obtener_resumen_gastos_dashboard(self):
        """Calcula el total gastado, el presupuesto total, el límite del 95% y el porcentaje consumido."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Total gastado acumulado
            cursor.execute("SELECT COALESCE(SUM(monto), 0) FROM gastos_efectuados")
            total_gastado = float(cursor.fetchone()[0] or 0.0)

            # 2. Total presupuestado acumulado
            cursor.execute("SELECT COALESCE(SUM(monto_presupuestado), 0) FROM categorias_egresos")
            total_presupuestado = float(cursor.fetchone()[0] or 0.0)

            # 3. Límite objetivo (95% del presupuesto)
            presupuesto_al_95 = total_presupuestado * 0.95

            # 4. Porcentaje consumido respecto al 95%
            if presupuesto_al_95 > 0:
                porcentaje = (total_gastado / presupuesto_al_95) * 100.0
            else:
                porcentaje = 0.0

            return {
                "total_gastado": total_gastado,
                "total_presupuestado": total_presupuestado,
                "presupuesto_al_95": presupuesto_al_95,
                "porcentaje": porcentaje
            }