"""Benchmark OLTP vs OLAP: SQLite vs DuckDB sobre ventas.csv (1,000,000 registros)."""
import csv, json, os, random, sqlite3, statistics, time
import duckdb

BASE  = os.path.dirname(os.path.abspath(__file__))
CSV   = os.path.join(BASE, "ventas.csv")
SQLDB = os.path.join(BASE, "ventas_sqlite.db")
DUCKF = os.path.join(BASE, "ventas_duck.db")

random.seed(7)
IDS      = [random.randint(1, 1_000_000) for _ in range(500)]   # venta_id: unico y ordenado
CLIENTES = [random.randint(1, 100_000) for _ in range(500)]     # cliente_id: NO ordenado

DDL_DUCK = """
CREATE TABLE ventas (
    venta_id        BIGINT,     -- sin PRIMARY KEY: asi NO existe indice implicito
    fecha           DATE,
    cliente_id      BIGINT,
    producto_id     BIGINT,
    categoria       VARCHAR,
    cantidad        BIGINT,
    precio_unitario DOUBLE,
    monto_total     DOUBLE,
    region          VARCHAR,
    canal           VARCHAR
)"""
DDL_SQ = (DDL_DUCK.replace("BIGINT", "INTEGER").replace("VARCHAR", "TEXT")
                  .replace("DOUBLE", "REAL").replace("DATE", "TEXT"))

def cronometrar(fn, reps, warmup=2):
    for _ in range(warmup):
        fn(0)
    t = []
    for i in range(reps):
        t0 = time.perf_counter(); fn(i); t.append((time.perf_counter() - t0) * 1000)
    return (statistics.mean(t), statistics.median(t), min(t), max(t))

# ------------------------------------------------------------------ carga
def cargar_sqlite():
    if os.path.exists(SQLDB): os.remove(SQLDB)
    con = sqlite3.connect(SQLDB); con.execute(DDL_SQ)
    t0 = time.perf_counter()
    with open(CSV) as f:
        r = csv.reader(f); next(r)
        con.executemany("INSERT INTO ventas VALUES (?,?,?,?,?,?,?,?,?,?)", r)
    con.commit(); dt = time.perf_counter() - t0
    con.execute("ANALYZE"); con.commit()
    return con, dt

def cargar_duckdb():
    if os.path.exists(DUCKF): os.remove(DUCKF)
    con = duckdb.connect(DUCKF); con.execute(DDL_DUCK)
    t0 = time.perf_counter()
    con.execute(f"INSERT INTO ventas SELECT * FROM read_csv('{CSV}', header=true)")
    dt = time.perf_counter() - t0
    con.execute("CHECKPOINT")
    return con, dt

print("Cargando SQLite...", flush=True); sq,  t_sq  = cargar_sqlite()
print("Cargando DuckDB...", flush=True); duk, t_duk = cargar_duckdb()

# ------------------------------------------------------------------ consultas
Q_ID  = ("SELECT venta_id, fecha, categoria, monto_total FROM ventas WHERE venta_id = {}")
Q_CLI = ("SELECT venta_id, fecha, categoria, monto_total FROM ventas WHERE cliente_id = {}")
Q_CAT = ("SELECT categoria, COUNT(*) AS n_ventas, SUM(monto_total) AS total, "
         "AVG(monto_total) AS ticket_prom FROM ventas GROUP BY categoria ORDER BY total DESC")
Q_MES_SQ  = ("SELECT strftime('%Y-%m', fecha) AS mes, COUNT(*) AS n_ventas, "
             "SUM(monto_total) AS total FROM ventas GROUP BY mes ORDER BY mes")
Q_MES_DUK = ("SELECT strftime(fecha, '%Y-%m') AS mes, COUNT(*) AS n_ventas, "
             "SUM(monto_total) AS total FROM ventas GROUP BY mes ORDER BY mes")

def r_sq(sql, params=None):
    return lambda i: sq.execute(sql.format(params[i % len(params)]) if params else sql).fetchall()
def r_du(sql, params=None):
    return lambda i: duk.execute(sql.format(params[i % len(params)]) if params else sql).fetchall()

R = {}
print("Q1  busqueda por venta_id SIN indice...", flush=True)
R["Q1_sqlite_sin_idx"]  = cronometrar(r_sq(Q_ID, IDS), 30)
R["Q1_duckdb_sin_idx"]  = cronometrar(r_du(Q_ID, IDS), 100)
print("Q1b busqueda por cliente_id (columna no ordenada) SIN indice...", flush=True)
R["Q1b_sqlite_sin_idx"] = cronometrar(r_sq(Q_CLI, CLIENTES), 30)
R["Q1b_duckdb_sin_idx"] = cronometrar(r_du(Q_CLI, CLIENTES), 100)
print("Q3  ventas por categoria...", flush=True)
R["Q3_sqlite"] = cronometrar(r_sq(Q_CAT), 15)
R["Q3_duckdb"] = cronometrar(r_du(Q_CAT), 15)
print("Q4  ventas por mes...", flush=True)
R["Q4_sqlite"] = cronometrar(r_sq(Q_MES_SQ), 15)
R["Q4_duckdb"] = cronometrar(r_du(Q_MES_DUK), 15)

print("CREATE INDEX...", flush=True)
t0 = time.perf_counter(); sq.execute("CREATE INDEX idx_ventas_id ON ventas(venta_id)"); sq.commit()
t_idx_sq = time.perf_counter() - t0
t0 = time.perf_counter(); duk.execute("CREATE INDEX idx_ventas_id ON ventas(venta_id)")
t_idx_du = time.perf_counter() - t0

print("Q2  busqueda por venta_id CON indice...", flush=True)
R["Q2_sqlite_con_idx"] = cronometrar(r_sq(Q_ID, IDS), 1000)
R["Q2_duckdb_con_idx"] = cronometrar(r_du(Q_ID, IDS), 500)

# ----- planes de ejecucion
sq.execute("DROP INDEX idx_ventas_id")
plan_sin = sq.execute("EXPLAIN QUERY PLAN " + Q_ID.format(500000)).fetchall()
plan_cat = sq.execute("EXPLAIN QUERY PLAN " + Q_CAT).fetchall()
sq.execute("CREATE INDEX idx_ventas_id ON ventas(venta_id)")
plan_con = sq.execute("EXPLAIN QUERY PLAN " + Q_ID.format(500000)).fetchall()
plan_duck_id  = duk.execute("EXPLAIN " + Q_ID.format(500000)).fetchall()[0][1]
plan_duck_cat = duk.execute("EXPLAIN " + Q_CAT).fetchall()[0][1]

# ----- resultados de negocio
cat_sq = sq.execute(Q_CAT).fetchall()
cat_du = duk.execute(Q_CAT).fetchall()
mes_du = duk.execute(Q_MES_DUK).fetchall()
iguales = all(a[0] == b[0] and a[1] == b[1] and abs(a[2]-b[2]) < 1 for a, b in zip(cat_sq, cat_du))

sq.commit(); sq.close(); duk.execute("CHECKPOINT"); duk.close()

out = {
  "entorno": {"sqlite": sqlite3.sqlite_version, "duckdb": duckdb.__version__},
  "carga_s":  {"sqlite": t_sq, "duckdb": t_duk},
  "indice_s": {"sqlite": t_idx_sq, "duckdb": t_idx_du},
  "tamano_mb": {"csv": os.path.getsize(CSV)/1e6, "sqlite": os.path.getsize(SQLDB)/1e6,
                "duckdb": os.path.getsize(DUCKF)/1e6},
  "tiempos_ms": {k: dict(zip(("media","mediana","min","max"), v)) for k, v in R.items()},
  "planes": {"sqlite_id_sin_idx": [list(r) for r in plan_sin],
             "sqlite_id_con_idx": [list(r) for r in plan_con],
             "sqlite_categoria":  [list(r) for r in plan_cat],
             "duckdb_id": plan_duck_id, "duckdb_categoria": plan_duck_cat},
  "resultados_iguales": iguales,
  "ventas_por_categoria": [list(r) for r in cat_sq],
  "ventas_por_mes": [[str(r[0]), r[1], r[2]] for r in mes_du],
}
json.dump(out, open(os.path.join(BASE, "resultados.json"), "w"), indent=2, default=str)

def fila(n, a, b):
    x, y = R[a][0], R[b][0]
    return f"{n:<40} {x:>11.3f} {y:>11.3f}   {(f'{x/y:>6.1f}x DuckDB' if y<x else f'{y/x:>6.1f}x SQLite')}"

print("\n" + "="*90)
print(f"RESULTADOS | 1,000,000 registros | SQLite {sqlite3.sqlite_version} | DuckDB {duckdb.__version__}")
print("="*90)
print(f"{'Consulta (media, ms)':<40} {'SQLite':>11} {'DuckDB':>11}   Mas rapido")
print("-"*90)
print(fila("Q1  ID sin indice",                  "Q1_sqlite_sin_idx",  "Q1_duckdb_sin_idx"))
print(fila("Q1b cliente_id sin indice (extra)",  "Q1b_sqlite_sin_idx", "Q1b_duckdb_sin_idx"))
print(fila("Q2  ID CON indice",                  "Q2_sqlite_con_idx",  "Q2_duckdb_con_idx"))
print(fila("Q3  Ventas por categoria",           "Q3_sqlite",          "Q3_duckdb"))
print(fila("Q4  Ventas por mes",                 "Q4_sqlite",          "Q4_duckdb"))
print("-"*90)
print(f"Carga 1M filas (s)    SQLite {t_sq:6.2f}  |  DuckDB {t_duk:6.2f}")
print(f"CREATE INDEX (s)      SQLite {t_idx_sq:6.2f}  |  DuckDB {t_idx_du:6.2f}")
print(f"Disco (MB)   CSV {out['tamano_mb']['csv']:.1f}  |  SQLite {out['tamano_mb']['sqlite']:.1f}"
      f"  |  DuckDB {out['tamano_mb']['duckdb']:.1f}")
print(f"Plan SQLite SIN indice : {plan_sin}")
print(f"Plan SQLite CON indice : {plan_con}")
print(f"Speedup del indice en SQLite (Q1 -> Q2): {R['Q1_sqlite_sin_idx'][0]/R['Q2_sqlite_con_idx'][0]:.0f}x")
print(f"Resultados identicos entre motores: {iguales}")
print("\nVENTAS POR CATEGORIA")
for c, n, tot, prom in cat_sq:
    print(f"  {c:<12} {n:>8,} ventas   total ${tot:>18,.0f}   ticket prom ${prom:>10,.0f}")
