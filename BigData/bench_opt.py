"""Experimento complementario: efecto de 4 optimizaciones concretas."""
import json, os, random, sqlite3, statistics, time
import duckdb

BASE = os.path.dirname(os.path.abspath(__file__))
sq  = sqlite3.connect(os.path.join(BASE, "ventas_sqlite.db"))
duk = duckdb.connect(os.path.join(BASE, "ventas_duck.db"))
random.seed(7)
IDS = [random.randint(1, 1_000_000) for _ in range(500)]

def crono(fn, reps, warmup=2):
    for _ in range(warmup): fn(0)
    t=[]
    for i in range(reps):
        t0=time.perf_counter(); fn(i); t.append((time.perf_counter()-t0)*1000)
    return statistics.mean(t)

R={}
# --- 1. Sentencia preparada (parametros ?) vs literal interpolado  [OLTP]
R["Q2_literal"]    = crono(lambda i: sq.execute(
    f"SELECT venta_id,fecha,categoria,monto_total FROM ventas WHERE venta_id = {IDS[i%500]}").fetchall(), 2000)
R["Q2_preparada"]  = crono(lambda i: sq.execute(
    "SELECT venta_id,fecha,categoria,monto_total FROM ventas WHERE venta_id = ?", (IDS[i%500],)).fetchall(), 2000)

# --- 2. Indice cubriente para la agregacion por categoria  [OLAP en motor de filas]
Q_CAT = ("SELECT categoria, COUNT(*), SUM(monto_total), AVG(monto_total) "
         "FROM ventas GROUP BY categoria ORDER BY 3 DESC")
R["Q3_sin_cubriente"] = crono(lambda i: sq.execute(Q_CAT).fetchall(), 10)
sq.execute("CREATE INDEX idx_cat_monto ON ventas(categoria, monto_total)"); sq.commit()
sq.execute("ANALYZE"); sq.commit()
R["Q3_con_cubriente"] = crono(lambda i: sq.execute(Q_CAT).fetchall(), 10)
plan_cub = sq.execute("EXPLAIN QUERY PLAN " + Q_CAT).fetchall()

# --- 3. Columna 'mes' materializada (evita strftime por fila)  [OLAP]
Q4_SQ = "SELECT strftime('%Y-%m',fecha) m, COUNT(*), SUM(monto_total) FROM ventas GROUP BY m ORDER BY m"
Q4_MAT= "SELECT mes m, COUNT(*), SUM(monto_total) FROM ventas GROUP BY m ORDER BY m"
R["Q4_strftime_sqlite"] = crono(lambda i: sq.execute(Q4_SQ).fetchall(), 10)
sq.execute("ALTER TABLE ventas ADD COLUMN mes TEXT")
sq.execute("UPDATE ventas SET mes = substr(fecha,1,7)"); sq.commit()
R["Q4_materializada_sqlite"] = crono(lambda i: sq.execute(Q4_MAT).fetchall(), 10)

Q4_DU = "SELECT strftime(fecha,'%Y-%m') m, COUNT(*), SUM(monto_total) FROM ventas GROUP BY m ORDER BY m"
R["Q4_strftime_duckdb"] = crono(lambda i: duk.execute(Q4_DU).fetchall(), 10)
duk.execute("ALTER TABLE ventas ADD COLUMN mes VARCHAR")
duk.execute("UPDATE ventas SET mes = strftime(fecha,'%Y-%m')")
R["Q4_materializada_duckdb"] = crono(lambda i: duk.execute(Q4_MAT).fetchall(), 10)

# --- 4. Tabla de resumen pre-agregada (vista materializada manual)  [OLAP]
sq.execute("CREATE TABLE resumen_mes AS " + Q4_MAT.replace("COUNT(*)","COUNT(*) n").replace("SUM(monto_total)","SUM(monto_total) total"))
sq.commit()
R["Q4_tabla_resumen_sqlite"] = crono(lambda i: sq.execute("SELECT * FROM resumen_mes ORDER BY m").fetchall(), 500)

sq.commit(); sq.close(); duk.close()
json.dump(R, open(os.path.join(BASE,"resultados_opt.json"),"w"), indent=2)

print("="*78); print("OPTIMIZACIONES ADICIONALES (tiempo medio, ms)"); print("="*78)
def l(a,b,na,nb):
    print(f"{na:<42}{R[a]:>9.3f}\n{nb:<42}{R[b]:>9.3f}   -> {R[a]/R[b]:.1f}x mas rapido\n")
l("Q2_literal","Q2_preparada","SQLite Q2 con literal interpolado","SQLite Q2 con sentencia preparada (?)")
l("Q3_sin_cubriente","Q3_con_cubriente","SQLite Q3 scan de tabla","SQLite Q3 con indice cubriente (categoria,monto)")
l("Q4_strftime_sqlite","Q4_materializada_sqlite","SQLite Q4 con strftime por fila","SQLite Q4 con columna 'mes' materializada")
l("Q4_strftime_duckdb","Q4_materializada_duckdb","DuckDB Q4 con strftime por fila","DuckDB Q4 con columna 'mes' materializada")
l("Q4_strftime_sqlite","Q4_tabla_resumen_sqlite","SQLite Q4 agregando 1M filas","SQLite Q4 leyendo tabla de resumen (36 filas)")
print("Plan SQLite Q3 con indice cubriente:", plan_cub)
