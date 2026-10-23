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
        """Crea la tabla de categorías de egresos si no existe."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categorias_egresos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    monto_presupuestado REAL DEFAULT 0.0
                )
            ''')
            
            # Categoría inicial por defecto si la tabla está vacía
            cursor.execute("SELECT COUNT(*) FROM categorias_egresos")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO categorias_egresos (nombre, monto_presupuestado) VALUES ('Miscelánea', 0.0)")
                
            conn.commit()

    def obtener_categorias_egresos(self):
        """Retorna la lista de categorías con sus presupuestos."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, monto_presupuestado FROM categorias_egresos ORDER BY id ASC")
            rows = cursor.fetchall()
            return [{"id": r[0], "nombre": r[1], "monto_presupuestado": r[2]} for r in rows]

    def agregar_categoria_egreso(self, nombre, monto_presupuestado):
        """Agrega una nueva categoría de egreso."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO categorias_egresos (nombre, monto_presupuestado) VALUES (?, ?)",
                (nombre.strip(), float(monto_presupuestado or 0.0))
            )
            conn.commit()

    def actualizar_categoria_egreso(self, id_cat, nuevo_nombre, nuevo_monto):
        """Actualiza el nombre y/o el monto presupuestado."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE categorias_egresos SET nombre = ?, monto_presupuestado = ? WHERE id = ?",
                (nuevo_nombre.strip(), float(nuevo_monto or 0.0), id_cat)
            )
            conn.commit()

    def eliminar_categoria_egreso(self, id_cat):
        """Elimina una categoría por su ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM categorias_egresos WHERE id = ?", (id_cat,))
            conn.commit()