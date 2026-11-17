"""
Graficos para el informe de la Actividad Practica 1 (INF3862, Clase 01).
OLTP vs OLAP: SQLite (motor de filas) contra DuckDB (motor de columnas)
sobre 1.000.000 de registros de ventas.

Lee   : resultados.json y resultados_opt.json (generados por bench.py y bench_opt.py)
Genera: graficos/*.png  en 200 dpi, fondo blanco, listos para pegar en Google Docs.

Uso:  python graficos.py
"""

import json
import os

import matplotlib
matplotlib.use("Agg")                      # sin ventana: solo escribe archivos
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "graficos")
os.makedirs(OUT, exist_ok=True)

# ----------------------------------------------------------------- paleta
# Dos colores categoricos validados para daltonismo (separacion CVD dE 24.6)
# y contraste >= 3:1 contra fondo blanco.
SQLITE = "#3E5C9A"      # azul tinta  - motor de filas
DUCKDB = "#C77A1A"      # ocre        - motor de columnas
NEUTRO = "#8B93A1"      # gris        - referencia / CSV
TINTA = "#16191F"       # texto principal
TINTA2 = "#434C5A"      # texto secundario
GRIS = "#D9DDE5"        # grillas y reglas

plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 11,
    "text.color": TINTA,
    "axes.labelcolor": TINTA2,
    "axes.edgecolor": GRIS,
    "xtick.color": TINTA2,
    "ytick.color": TINTA2,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.titlepad": 14,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 200,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.3,
})


def cargar(nombre):
    ruta = os.path.join(BASE, nombre)
    if not os.path.exists(ruta):
        raise SystemExit(
            f"Falta {nombre} en {BASE}.\n"
            "Ejecute primero bench.py y bench_opt.py para generarlo."
        )
    with open(ruta) as f:
        return json.load(f)


R = cargar("resultados.json")
OPT = cargar("resultados_opt.json")
T = R["tiempos_ms"]


def ms(clave):
    """Tiempo medio en milisegundos de una consulta medida."""
    return T[clave]["media"]


def es(v, dec=1):
    """Numero con formato chileno: punto para miles, coma para decimales."""
    return (f"{v:,.{dec}f}"
            .replace(",", " ")      # separador de miles, reservado
            .replace(".", ",")           # decimal
            .replace(" ", "."))     # miles definitivo


def etiqueta_ms(v):
    """Formatea un tiempo para mostrarlo junto a la marca."""
    if v < 0.1:
        return es(v, 3) + " ms"
    if v < 10:
        return es(v, 2) + " ms"
    return es(v, 1) + " ms"


def coma(v, _=None):
    """Formateador de ejes: 13.0 -> 13,0  ·  1000 -> 1000."""
    return f"{v:g}".replace(".", ",")


def guardar(fig, nombre):
    ruta = os.path.join(OUT, nombre)
    fig.savefig(ruta)
    plt.close(fig)
    print(f"  escrito  graficos/{nombre}")


def pie(ax, texto, dy=-0.16):
    """Nota al pie de la figura, en gris, bajo el eje."""
    ax.annotate(texto, xy=(0, dy), xycoords="axes fraction",
                fontsize=8.5, color=NEUTRO, va="top")


# =====================================================================
# 1. Tiempo por consulta en ambos motores
#    Grafico de puntos sobre eje logaritmico: con 4 ordenes de magnitud
#    de diferencia, la posicion codifica el tiempo sin que las barras
#    exageren la comparacion (una barra en escala log miente de largo).
# =====================================================================
CONSULTAS = [
    ("Q1  Busqueda por ID\nsin indice",        "Q1_sqlite_sin_idx",  "Q1_duckdb_sin_idx"),
    ("Q2  Busqueda por ID\ncon indice",        "Q2_sqlite_con_idx",  "Q2_duckdb_con_idx"),
    ("Q3  Ventas por categoria\nGROUP BY",     "Q3_sqlite",          "Q3_duckdb"),
    ("Q4  Ventas por mes\nGROUP BY",           "Q4_sqlite",          "Q4_duckdb"),
    ("Extra  Busqueda por cliente_id\nsin indice", "Q1b_sqlite_sin_idx", "Q1b_duckdb_sin_idx"),
]


def grafico_1_tiempos():
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    y = range(len(CONSULTAS))

    for i, (_, k_sq, k_du) in enumerate(CONSULTAS):
        a, b = ms(k_sq), ms(k_du)
        ax.plot([min(a, b), max(a, b)], [i, i], color=GRIS, lw=2, zorder=1)
        ax.scatter([a], [i], s=130, color=SQLITE, zorder=3,
                   edgecolors="white", linewidths=1.6)
        ax.scatter([b], [i], s=130, color=DUCKDB, zorder=3,
                   edgecolors="white", linewidths=1.6)
        # etiqueta directa: el valor de cada motor, al lado que no se solapa
        izq, der = (a, b) if a < b else (b, a)
        ax.annotate(etiqueta_ms(izq), xy=(izq, i), xytext=(-9, 0),
                    textcoords="offset points", ha="right", va="center",
                    fontsize=9, color=TINTA2)
        ax.annotate(etiqueta_ms(der), xy=(der, i), xytext=(9, 0),
                    textcoords="offset points", ha="left", va="center",
                    fontsize=9, color=TINTA2)
        # razon entre ambos, centrada sobre el conector
        razon = max(a, b) / min(a, b)
        ganador = "SQLite" if a < b else "DuckDB"
        centro = (min(a, b) * max(a, b)) ** 0.5      # punto medio en escala log
        ax.annotate(f"{es(razon)}x {ganador}",
                    xy=(centro, i), xytext=(0, 13), textcoords="offset points",
                    ha="center", fontsize=8.5, color=TINTA2,
                    bbox=dict(boxstyle="round,pad=0.28", fc="white",
                              ec=GRIS, lw=0.8))

    ax.set_xscale("log")
    ax.set_yticks(list(y))
    ax.set_yticklabels([c[0] for c in CONSULTAS], fontsize=9.5)
    # banda libre bajo la ultima fila para que la leyenda no pise las etiquetas
    ax.set_ylim(len(CONSULTAS) - 1 + 0.95, -0.62)
    ax.set_xlim(0.0024, 2200)
    ax.set_xlabel("Tiempo medio por consulta (ms, escala logaritmica)")
    ax.xaxis.set_major_formatter(FuncFormatter(coma))
    ax.grid(axis="x", color=GRIS, lw=0.8, alpha=0.9)
    ax.set_axisbelow(True)
    ax.set_title("Tiempo por consulta: SQLite contra DuckDB\n"
                 "1.000.000 de registros de ventas", loc="left")

    ax.scatter([], [], s=110, color=SQLITE, label="SQLite  ·  motor de filas")
    ax.scatter([], [], s=110, color=DUCKDB, label="DuckDB  ·  motor de columnas")
    ax.legend(frameon=False, loc="lower right", fontsize=9.5)
    pie(ax, "Media de 15 a 1.000 repeticiones con cache caliente. Mas a la izquierda "
            "es mas rapido.")
    guardar(fig, "01_tiempos_por_consulta.png")


# =====================================================================
# 2. Efecto del indice sobre la busqueda puntual (pregunta 3)
# =====================================================================
def grafico_2_indice():
    sin_idx, con_idx = ms("Q1_sqlite_sin_idx"), ms("Q2_sqlite_con_idx")
    fig, ax = plt.subplots(figsize=(9, 3.4))

    ax.annotate("", xy=(con_idx, 0), xytext=(sin_idx, 0),
                arrowprops=dict(arrowstyle="-|>", color=SQLITE, lw=2.4,
                                shrinkA=9, shrinkB=9))
    ax.scatter([sin_idx], [0], s=190, color=NEUTRO, zorder=3,
               edgecolors="white", linewidths=2)
    ax.scatter([con_idx], [0], s=190, color=SQLITE, zorder=3,
               edgecolors="white", linewidths=2)

    ax.annotate(f"SCAN ventas\n{etiqueta_ms(sin_idx)}", xy=(sin_idx, 0),
                xytext=(0, 26), textcoords="offset points", ha="center",
                fontsize=10, color=TINTA, linespacing=1.5)
    ax.annotate(f"SEARCH USING INDEX\n{etiqueta_ms(con_idx)}", xy=(con_idx, 0),
                xytext=(0, 26), textcoords="offset points", ha="center",
                fontsize=10, color=SQLITE, fontweight="bold", linespacing=1.5)
    centro = (sin_idx * con_idx) ** 0.5
    ax.annotate(f"{es(sin_idx / con_idx, 0)}x mas rapido",
                xy=(centro, 0), xytext=(0, -28), textcoords="offset points",
                ha="center", fontsize=12, fontweight="bold", color=SQLITE)

    ax.set_xscale("log")
    ax.set_xlim(0.0045, 95)
    ax.set_ylim(-0.42, 0.5)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("Tiempo de la busqueda por venta_id en SQLite (ms, escala logaritmica)")
    ax.xaxis.set_major_formatter(FuncFormatter(coma))
    ax.grid(axis="x", color=GRIS, lw=0.8)
    ax.set_axisbelow(True)
    ax.set_title("Efecto del indice sobre una busqueda puntual (SQLite)", loc="left")
    pie(ax, "El plan de ejecucion cambia de recorrer 1.000.000 de filas a descender "
            "unos 20 niveles de un arbol B.", dy=-0.34)
    guardar(fig, "02_efecto_del_indice.png")


# =====================================================================
# 3. Quien gana cada consulta y por cuanto (grafico divergente)
# =====================================================================
def grafico_3_ventaja():
    etiquetas, valores, colores = [], [], []
    for nombre, k_sq, k_du in CONSULTAS:
        a, b = ms(k_sq), ms(k_du)
        razon = max(a, b) / min(a, b)
        etiquetas.append(nombre.replace("\n", " · "))
        # positivo = gana DuckDB (derecha); negativo = gana SQLite (izquierda)
        valores.append(razon if b < a else -razon)
        colores.append(DUCKDB if b < a else SQLITE)

    fig, ax = plt.subplots(figsize=(9.5, 4.4))
    barras = ax.barh(range(len(valores)), valores, color=colores, height=0.58)
    for i, (barra, v) in enumerate(zip(barras, valores)):
        off = 8 if v > 0 else -8
        ax.annotate(f"{es(abs(v))}x",
                    xy=(v, i), xytext=(off, 0), textcoords="offset points",
                    ha="left" if v > 0 else "right", va="center",
                    fontsize=10, fontweight="bold",
                    color=DUCKDB if v > 0 else SQLITE)

    ax.axvline(0, color=TINTA, lw=1.2)
    ax.set_yticks(range(len(etiquetas)))
    ax.set_yticklabels(etiquetas, fontsize=9.5)
    # banda libre sobre la primera barra para rotular cada lado del eje cero
    ax.set_ylim(len(valores) - 0.45, -1.15)
    ax.set_xlim(-45, 175)
    ax.set_xticks([-40, -20, 0, 50, 100, 150])
    ax.set_xticklabels(["40x", "20x", "0", "50x", "100x", "150x"])
    ax.set_xlabel("Cuantas veces mas rapido fue el motor ganador")
    ax.grid(axis="x", color=GRIS, lw=0.8)
    ax.set_axisbelow(True)
    ax.set_title("Que motor gana cada consulta", loc="left")
    ax.annotate("gana SQLite  <", xy=(-3, -0.88), ha="right", va="center",
                fontsize=9.5, color=SQLITE, fontweight="bold")
    ax.annotate(">  gana DuckDB", xy=(3, -0.88), ha="left", va="center",
                fontsize=9.5, color=DUCKDB, fontweight="bold")
    pie(ax, "Ningun motor gana siempre: DuckDB domina las agregaciones, SQLite "
            "domina la busqueda puntual indexada.")
    guardar(fig, "03_que_motor_gana.png")


# =====================================================================
# 4. Costo de construir la base: disco y tiempo de carga
# =====================================================================
def grafico_4_almacenamiento():
    tam = R["tamano_mb"]
    carga = R["carga_s"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.8, 3.8),
                                   gridspec_kw={"width_ratios": [1.35, 1]})

    etiquetas = ["CSV original", "SQLite", "DuckDB"]
    valores = [tam["csv"], tam["sqlite"], tam["duckdb"]]
    ax1.barh(etiquetas, valores, color=[NEUTRO, SQLITE, DUCKDB], height=0.46)
    for i, v in enumerate(valores):
        ax1.annotate(f"{v:,.1f} MB".replace(".", ","), xy=(v, i), xytext=(7, 0),
                     textcoords="offset points", va="center", fontsize=10,
                     color=TINTA2)
    ax1.invert_yaxis()
    ax1.set_xlim(0, max(valores) * 1.25)
    ax1.set_xlabel("Espacio en disco (MB)")
    ax1.xaxis.set_major_formatter(FuncFormatter(coma))
    ax1.grid(axis="x", color=GRIS, lw=0.8)
    ax1.set_axisbelow(True)
    ax1.set_title("La misma tabla en disco", loc="left", fontsize=12)

    etiquetas2 = ["SQLite", "DuckDB"]
    valores2 = [carga["sqlite"], carga["duckdb"]]
    ax2.barh(etiquetas2, valores2, color=[SQLITE, DUCKDB], height=0.38)
    for i, v in enumerate(valores2):
        ax2.annotate(f"{v:,.2f} s".replace(".", ","), xy=(v, i), xytext=(7, 0),
                     textcoords="offset points", va="center", fontsize=10,
                     color=TINTA2)
    ax2.invert_yaxis()
    ax2.set_xlim(0, max(valores2) * 1.35)
    ax2.set_xlabel("Tiempo de carga (s)")
    ax2.xaxis.set_major_formatter(FuncFormatter(coma))
    ax2.grid(axis="x", color=GRIS, lw=0.8)
    ax2.set_axisbelow(True)
    ax2.set_title("Cargar 1.000.000 de filas", loc="left", fontsize=12)

    fig.suptitle("Costo de construir la base de datos", x=0.062, y=1.06,
                 ha="left", fontsize=14, fontweight="bold")
    ax1.annotate("DuckDB comprime por columna: diccionario para categoria, region y "
                 "canal;\ndiferencias para los enteros consecutivos.",
                 xy=(0, -0.3), xycoords="axes fraction", fontsize=8.5,
                 color=NEUTRO, va="top")
    guardar(fig, "04_almacenamiento_y_carga.png")


# =====================================================================
# 5. Poda de columnas: que lee cada consulta de la tabla de 10 columnas
#    (lamina 25-26 de la clase: por filas contra por columnas)
# =====================================================================
def grafico_5_columnas():
    columnas = ["venta_id", "fecha", "cliente_id", "producto_id", "categoria",
                "cantidad", "precio_unitario", "monto_total", "region", "canal"]
    consultas = {
        "Q1 / Q2  Busqueda por ID": ["venta_id", "fecha", "categoria", "monto_total"],
        "Q3  Ventas por categoria": ["categoria", "monto_total"],
        "Q4  Ventas por mes": ["fecha", "monto_total"],
    }

    fig, ax = plt.subplots(figsize=(9.8, 3.6))
    for fila, (nombre, usadas) in enumerate(consultas.items()):
        for col, nombre_col in enumerate(columnas):
            leida = nombre_col in usadas
            ax.add_patch(plt.Rectangle(
                (col + 0.06, fila + 0.12), 0.88, 0.76,
                facecolor=DUCKDB if leida else "white",
                edgecolor=DUCKDB if leida else GRIS,
                linewidth=1.2))
        ax.annotate(f"{len(usadas)} de 10", xy=(10.2, fila + 0.5), va="center",
                    fontsize=10, fontweight="bold", color=DUCKDB)

    ax.set_xlim(0, 11.6)
    ax.set_ylim(0, len(consultas))
    ax.invert_yaxis()
    ax.set_xticks([i + 0.5 for i in range(len(columnas))])
    ax.set_xticklabels(columnas, rotation=38, ha="right", fontsize=9)
    ax.set_yticks([i + 0.5 for i in range(len(consultas))])
    ax.set_yticklabels(list(consultas), fontsize=10)
    ax.tick_params(length=0)
    for lado in ("top", "right", "bottom", "left"):
        ax.spines[lado].set_visible(False)
    ax.set_title("Poda de columnas: que lee realmente cada consulta", loc="left")
    pie(ax, "Un motor columnar lee solo los bloques coloreados. Un motor de filas debe "
            "leer y decodificar el registro completo,\nincluidas las columnas que "
            "descarta. La ventaja crece con el ancho de la tabla.", dy=-0.50)
    guardar(fig, "05_poda_de_columnas.png")


# =====================================================================
# 6. Optimizaciones adicionales medidas (pregunta 5)
# =====================================================================
def grafico_6_optimizaciones():
    pares = [
        ("Sentencia preparada\nSQLite · busqueda por ID",
         OPT["Q2_literal"], OPT["Q2_preparada"]),
        ("Indice cubriente (categoria, monto)\nSQLite · ventas por categoria",
         OPT["Q3_sin_cubriente"], OPT["Q3_con_cubriente"]),
        ("Columna 'mes' materializada\nDuckDB · ventas por mes",
         OPT["Q4_strftime_duckdb"], OPT["Q4_materializada_duckdb"]),
        ("Tabla de resumen pre-agregada\nSQLite · ventas por mes",
         OPT["Q4_strftime_sqlite"], OPT["Q4_tabla_resumen_sqlite"]),
    ]

    fig, ax = plt.subplots(figsize=(9.5, 4.6))
    for i, (nombre, antes, despues) in enumerate(pares):
        ax.annotate("", xy=(despues, i), xytext=(antes, i),
                    arrowprops=dict(arrowstyle="-|>", color=TINTA2, lw=2,
                                    shrinkA=8, shrinkB=8))
        ax.scatter([antes], [i], s=120, color=NEUTRO, zorder=3,
                   edgecolors="white", linewidths=1.6)
        ax.scatter([despues], [i], s=120, color=DUCKDB, zorder=3,
                   edgecolors="white", linewidths=1.6)
        ax.annotate(etiqueta_ms(antes), xy=(antes, i), xytext=(10, 0),
                    textcoords="offset points", va="center", fontsize=9,
                    color=TINTA2)
        ax.annotate(etiqueta_ms(despues), xy=(despues, i), xytext=(-10, 0),
                    textcoords="offset points", ha="right", va="center",
                    fontsize=9, color=TINTA2)
        centro = (antes * despues) ** 0.5
        ax.annotate(f"{es(antes / despues)}x",
                    xy=(centro, i), xytext=(0, 14), textcoords="offset points",
                    ha="center", fontsize=9.5, fontweight="bold", color=TINTA,
                    bbox=dict(boxstyle="round,pad=0.26", fc="white", ec=GRIS, lw=0.8))

    ax.set_xscale("log")
    ax.set_yticks(range(len(pares)))
    ax.set_yticklabels([p[0] for p in pares], fontsize=9.5)
    # banda libre bajo la ultima fila para la leyenda
    ax.set_ylim(len(pares) - 1 + 0.95, -0.55)
    ax.set_xlim(0.0011, 5000)
    ax.set_xlabel("Tiempo medio de la consulta (ms, escala logaritmica)")
    ax.xaxis.set_major_formatter(FuncFormatter(coma))
    ax.grid(axis="x", color=GRIS, lw=0.8)
    ax.set_axisbelow(True)
    ax.set_title("Optimizaciones adicionales medidas", loc="left")
    ax.scatter([], [], s=110, color=NEUTRO, label="antes")
    ax.scatter([], [], s=110, color=DUCKDB, label="despues")
    ax.legend(frameon=False, loc="lower right", fontsize=9.5)
    pie(ax, "Comparaciones pareadas dentro de una misma ejecucion; los valores "
            "absolutos no son comparables con la tabla principal.")
    guardar(fig, "06_optimizaciones.png")


# =====================================================================
# 7. Resultado de negocio de Q3: ventas por categoria
# =====================================================================
def miles(n):
    """Separador de miles con punto, al estilo chileno."""
    return f"{n:,}".replace(",", ".")


def grafico_7_categorias():
    datos = sorted(R["ventas_por_categoria"], key=lambda r: r[2], reverse=True)
    nombres = [d[0] for d in datos]
    totales = [d[2] / 1e9 for d in datos]        # miles de millones de pesos
    conteos = [d[1] for d in datos]

    fig, ax = plt.subplots(figsize=(9.2, 4.2))
    ax.bar(nombres, totales, color=DUCKDB, width=0.52)
    for i, (t, n) in enumerate(zip(totales, conteos)):
        ax.annotate("$" + es(t) + " mil mill.",
                    xy=(i, t), xytext=(0, 7), textcoords="offset points",
                    ha="center", fontsize=9.5, color=TINTA)
        ax.annotate(miles(n) + " ventas", xy=(i, 0), xytext=(0, 9),
                    textcoords="offset points", ha="center", fontsize=8.5,
                    color="white")
    ax.set_ylim(0, max(totales) * 1.18)
    ax.set_ylabel("Monto total vendido (miles de millones de CLP)")
    ax.yaxis.set_major_formatter(FuncFormatter(coma))
    ax.grid(axis="y", color=GRIS, lw=0.8)
    ax.set_axisbelow(True)
    ax.set_title("Resultado de Q3: ventas por categoria", loc="left")
    pie(ax, "Salida real de la consulta OLAP: 1.000.000 de filas agregadas en 5 grupos. "
            "DuckDB la resuelve en 1,56 ms.")
    guardar(fig, "07_ventas_por_categoria.png")


# =====================================================================
# 8. Resultado de negocio de Q4: ventas por mes
# =====================================================================
def grafico_8_meses():
    datos = R["ventas_por_mes"]
    meses = [d[0] for d in datos]
    totales = [d[2] / 1e9 for d in datos]

    fig, ax = plt.subplots(figsize=(9.8, 4.0))
    # linea sin relleno: el eje no parte en cero, y un area bajo un eje truncado
    # exagera visualmente la variacion
    ax.plot(range(len(meses)), totales, color=DUCKDB, lw=2, zorder=3)

    i_max = totales.index(max(totales))
    i_min = totales.index(min(totales))
    for i, color, texto in ((i_max, DUCKDB, "maximo"), (i_min, NEUTRO, "minimo")):
        ax.scatter([i], [totales[i]], s=90, color=color, zorder=4,
                   edgecolors="white", linewidths=1.6)
        ax.annotate(f"{texto}  {meses[i]}\n$" + es(totales[i]) + " mil mill.",
                    xy=(i, totales[i]), xytext=(0, 16 if i == i_max else -36),
                    textcoords="offset points", ha="center", fontsize=9,
                    color=TINTA2, linespacing=1.4)

    ax.set_xticks(range(0, len(meses), 3))
    ax.set_xticklabels([meses[i] for i in range(0, len(meses), 3)],
                       rotation=45, ha="right", fontsize=9)
    ax.set_ylim(min(totales) * 0.93, max(totales) * 1.05)
    ax.set_ylabel("Monto vendido (miles de millones de CLP)")
    ax.yaxis.set_major_formatter(FuncFormatter(coma))
    ax.grid(axis="y", color=GRIS, lw=0.8)
    ax.set_axisbelow(True)
    ax.set_title("Resultado de Q4: ventas por mes, 2023 a 2025", loc="left")
    pie(ax, "36 grupos derivados de la columna fecha. El eje vertical no parte en cero. "
            "En SQLite esta consulta tarda 350,7 ms; en DuckDB, 4,98 ms.", dy=-0.38)
    guardar(fig, "08_ventas_por_mes.png")


if __name__ == "__main__":
    print(f"Generando graficos en {OUT}")
    grafico_1_tiempos()
    grafico_2_indice()
    grafico_3_ventaja()
    grafico_4_almacenamiento()
    grafico_5_columnas()
    grafico_6_optimizaciones()
    grafico_7_categorias()
    grafico_8_meses()
    print("Listo. 8 graficos en 200 dpi, listos para insertar en Google Docs.")
