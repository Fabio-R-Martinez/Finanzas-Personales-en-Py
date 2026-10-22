-- src/database/schema.sql

PRAGMA foreign_keys = ON;

-- 1. Tabla de Categorías (Alimentación, Transporte, Sueldo, etc.)
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    tipo TEXT CHECK(tipo IN ('INGRESO', 'GASTO')) NOT NULL
);

-- 2. Tabla de Presupuestos Planificados (Límite o Meta mensual por categoría)
CREATE TABLE IF NOT EXISTS presupuestos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    periodo TEXT NOT NULL, -- Formato 'YYYY-MM' (ej. '2026-09')
    categoria_id INTEGER NOT NULL,
    monto_esperado INTEGER NOT NULL CHECK(monto_esperado >= 0),
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE,
    UNIQUE(periodo, categoria_id)
);

-- 3. Tabla de Transacciones Reales (Compras, pagos o ingresos ejecutados)
CREATE TABLE IF NOT EXISTS transacciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria_id INTEGER NOT NULL,
    monto_ejecutado INTEGER NOT NULL CHECK(monto_ejecutado >= 0),
    fecha TEXT NOT NULL, -- Formato 'YYYY-MM-DD'
    notas TEXT,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE
);
```

Vinculación con `db_manager.py`:

Para que `DBManager` lea este archivo directamente desde el disco al inicializarse, puedes actualizar el método `_inicializar_tablas()` en **src/database/db_manager.py**:

```
from pathlib import Path

def _inicializar_tablas(self):
    """Crea las tablas leyendo las instrucciones desde schema.sql."""
    schema_path = Path(__file__).parent / "schema.sql"
    if schema_path.exists():
        with open(schema_path, "r", encoding="utf-8") as f:
            ddl_script = f.read()
        with self.get_connection() as conn:
            conn.executescript(ddl_script)
