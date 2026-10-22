"""

2. Diseño de Tablas SQL e Implementación en SQLite
Para garantizar persistencia offline ligera, se separan los presupuestos planificados (asociados al periodo YYYY-MM) de los movimientos reales ejecutados (asociados a una fecha exacta YYYY-MM-DD).
Esquema DDL de Base de Datos
"""

-- Active Foreign Keys para integridad referencial
PRAGMA foreign_keys = ON;

-- 1. Tabla de Categorias
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    tipo TEXT CHECK(tipo IN ('INGRESO', 'GASTO')) NOT NULL
);

-- 2. Tabla de Presupuestos Planificados (Esperados por periodo)
CREATE TABLE IF NOT EXISTS presupuestos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    periodo TEXT NOT NULL, -- Ej: '2026-09'
    categoria_id INTEGER NOT NULL,
    monto_esperado REAL NOT NULL CHECK(monto_esperado >= 0),
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE,
    UNIQUE(periodo, categoria_id) -- Un unico presupuesto por categoria por mes
);

-- 3. Tabla de Transacciones Reales (Movimientos Efectuados)
CREATE TABLE IF NOT EXISTS transacciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria_id INTEGER NOT NULL,
    monto_ejecutado REAL NOT NULL CHECK(monto_ejecutado >= 0),
    fecha TEXT NOT NULL, -- Ej: '2026-09-05'
    notas TEXT,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE
);

Consulta SQL Consolidada (CTE con Agragación por Período)
La siguiente consulta utiliza Common Table Expressions (CTE) con LEFT JOIN y COALESCE para unir lo planificado con lo ejecutado en un periodo específico (2026-09), manejando casos borde (categorías presupuestadas sin gastos reales, o gastos imprevistos no presupuestados):
|
WITH 
P AS (
    SELECT categoria_id, SUM(monto_esperado) AS total_esperado
    FROM presupuestos
    WHERE periodo = '2026-09'
    GROUP BY categoria_id
),
T AS (
    SELECT categoria_id, SUM(monto_ejecutado) AS total_ejecutado
    FROM transacciones
    WHERE strftime('%Y-%m', fecha) = '2026-09'
    GROUP BY categoria_id
)
SELECT 
    c.id AS categoria_id,
    c.nombre AS categoria,
    c.tipo,
    COALESCE(P.total_esperado, 0.0) AS monto_esperado,
    COALESCE(T.total_ejecutado, 0.0) AS monto_ejecutado,
    (COALESCE(T.total_ejecutado, 0.0) - COALESCE(P.total_esperado, 0.0)) AS diferencia
FROM categorias c
LEFT JOIN P ON c.id = P.categoria_id
LEFT JOIN T ON c.id = T.categoria_id
WHERE P.categoria_id IS NOT NULL OR T.categoria_id IS NOT NULL
ORDER BY c.tipo DESC, c.nombre ASC;
