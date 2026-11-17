"""
Actividad 2 - INF3862 Big Data | ETL de ventas orquestado con Dagster.

Pipeline de 5 activos de datos (assets) que implementa Extract -> Transform -> Load
sobre archivos locales, aplicando las tecnicas de transformacion de la Clase 02.

    ventas_crudas ────────────┐
                              ├──> ventas_limpias ──> ventas_por_categoria_mes ──┐
    catalogo_productos ───────┘         │                                        │
                                        └──> ventas_cuarentena                   │
                                                                                 │
                              warehouse_ventas (DuckDB local) <──────────────────┘

Tecnicas de transformacion aplicadas (Clase 02):

    T1  Limpiar            espacios sobrantes en todos los campos de texto
    T2  Estandarizar       estado: " PAGADO ", "paid", "Pagado" -> "pagado"
    T3  Estandarizar       fecha: dd/mm/aaaa y ISO -> date
    T4  Estandarizar       precio: "19.990" y "19990" -> 19990 (entero, CLP)
    T5  Estandarizar       peso: "1200 g" y "1.2 kg" -> 1.2 (kg)
    T6  Splitting          codigo_pedido "SCL-2026-00981" -> sucursal, anio, numero
    T7  Deduplicar         por clave (codigo_pedido, linea), conservando una copia
    T8  Limpiar            cantidad vacia -> CUARENTENA (no se asume cantidad = 0)
    T9  Derivar            importe = cantidad x precio_unitario
    T10 Joining            con el catalogo, controlando cardinalidad y sin match
    T11 Cifrar/proteger    email -> seudonimo HMAC-SHA256 (el email no se carga)
    T12 Resumir            cambio de grano: linea de venta -> categoria x mes

Verificacion: cada asset publica metadata en la UI y hay 7 asset checks que validan
el resultado, incluido un cuadre contra el manifiesto de suciedad plantada
(data/raw/_manifiesto_suciedad.json) y un cuadre detalle-vs-resumen.

Ejecutar:  dg dev   ->   http://localhost:3000   ->   Assets -> Materialize all
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
from pathlib import Path

import dagster as dg
import duckdb
import pandas as pd

# --------------------------------------------------------------------------- rutas
RAIZ = Path(__file__).resolve().parents[3]
RAW = RAIZ / "data" / "raw"
STAGING = RAIZ / "data" / "staging"
PROCESSED = RAIZ / "data" / "processed"
WAREHOUSE = RAIZ / "data" / "warehouse"

F_VENTAS_RAW = RAW / "ventas_crudas.csv"
F_CATALOGO_RAW = RAW / "catalogo_productos.csv"
F_MANIFIESTO = RAW / "_manifiesto_suciedad.json"
F_VENTAS_STG = STAGING / "ventas_crudas.parquet"
F_CATALOGO_STG = STAGING / "catalogo_productos.parquet"
F_LIMPIAS = PROCESSED / "ventas_limpias.parquet"
F_CUARENTENA = PROCESSED / "ventas_cuarentena.csv"
F_RESUMEN = PROCESSED / "ventas_por_categoria_mes.csv"
F_DUCKDB = WAREHOUSE / "ventas.duckdb"

CLAVE = ["codigo_pedido", "linea"]
ESTADOS_VALIDOS = {"pagado", "pendiente", "anulado"}
# El origen escribe el mismo estado en espaniol y en ingles.
MAPA_ESTADOS = {"paid": "pagado", "cancelled": "anulado", "canceled": "anulado"}

# Clave de seudonimizacion. En produccion vendria de un gestor de secretos; aqui se
# lee del entorno con un valor por defecto solo para que la actividad sea reproducible.
CLAVE_SEUDONIMO = os.environ.get("ETL_CLAVE_SEUDONIMO", "inf3862-demo").encode()


def _md(df: pd.DataFrame, n: int = 5) -> dg.MetadataValue:
    """Tabla markdown para previsualizar un DataFrame en la UI de Dagster."""
    return dg.MetadataValue.md(df.head(n).to_markdown(index=False))


# =============================================================== EXTRACT ==========
@dg.asset(
    group_name="extract",
    description="Extract: lee ventas_crudas.csv tal como llega del origen, sin "
                "transformar, y lo deja en staging como Parquet.",
)
def ventas_crudas() -> dg.MaterializeResult:
    STAGING.mkdir(parents=True, exist_ok=True)

    # Todo se lee como texto y sin interpretar vacios: la interpretacion de tipos es
    # una decision del paso Transform, no del lector de CSV. Si pandas adivinara los
    # tipos aqui, perderiamos la evidencia de como venia el dato.
    df = pd.read_csv(F_VENTAS_RAW, dtype=str, keep_default_na=False)
    df.to_parquet(F_VENTAS_STG, index=False)

    vacios = {c: int((df[c].str.strip() == "").sum()) for c in df.columns}
    return dg.MaterializeResult(
        metadata={
            "filas": len(df),
            "columnas": len(df.columns),
            "origen": str(F_VENTAS_RAW.relative_to(RAIZ)),
            "destino": str(F_VENTAS_STG.relative_to(RAIZ)),
            "campos_con_vacios": dg.MetadataValue.json(
                {k: v for k, v in vacios.items() if v}
            ),
            "muestra": _md(df),
        }
    )


@dg.asset(
    group_name="extract",
    description="Extract + control de cardinalidad: lee el catalogo y resuelve los "
                "producto_id repetidos ANTES del join, para que el join no duplique "
                "ventas (advertencia explicita de la Clase 02).",
)
def catalogo_productos() -> dg.MaterializeResult:
    STAGING.mkdir(parents=True, exist_ok=True)
    cat = pd.read_csv(F_CATALOGO_RAW, dtype=str, keep_default_na=False)
    n_entrada = len(cat)

    # Un producto_id repetido puede ser de dos clases muy distintas:
    #   - duplicado exacto      -> es ruido, se conserva una copia
    #   - duplicado en conflicto -> dos verdades distintas para el mismo producto;
    #                               hace falta una REGLA DE NEGOCIO, no un dropna.
    exactos = cat[cat.duplicated(keep="first")]
    sin_exactos = cat.drop_duplicates(keep="first")
    en_conflicto = sin_exactos[sin_exactos.duplicated(subset=["producto_id"], keep=False)]

    # Regla elegida y declarada: ante conflicto se conserva la PRIMERA aparicion del
    # archivo (orden de llegada). Queda registrada en la metadata para que sea auditable.
    cat_final = sin_exactos.drop_duplicates(subset=["producto_id"], keep="first").copy()
    cat_final["producto_id"] = cat_final["producto_id"].astype("int64")
    cat_final["precio_lista"] = cat_final["precio_lista"].astype("int64")
    cat_final.to_parquet(F_CATALOGO_STG, index=False)

    return dg.MaterializeResult(
        metadata={
            "filas_entrada": n_entrada,
            "productos_unicos": len(cat_final),
            "duplicados_exactos_eliminados": len(exactos),
            "producto_id_en_conflicto": len(en_conflicto["producto_id"].unique()),
            "detalle_conflictos": dg.MetadataValue.md(
                en_conflicto.to_markdown(index=False) if len(en_conflicto)
                else "_sin conflictos_"
            ),
            "regla_de_resolucion": "conservar la primera aparicion del archivo",
            "muestra": _md(cat_final),
        }
    )


# ============================================================= TRANSFORM ==========
@dg.multi_asset(
    specs=[
        dg.AssetSpec(
            "ventas_limpias",
            deps=["ventas_crudas", "catalogo_productos"],
            group_name="transform",
            description="Transform: aplica T1-T11. Producto de datos principal, "
                        "listo para analisis.",
        ),
        dg.AssetSpec(
            "ventas_cuarentena",
            deps=["ventas_crudas"],
            group_name="transform",
            description="Transform: filas que NO se pueden interpretar con certeza. "
                        "Se aislan para revision humana en vez de imputarlas.",
        ),
    ]
)
def transformar_ventas():
    PROCESSED.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet(F_VENTAS_STG)
    cat = pd.read_parquet(F_CATALOGO_STG)
    n_entrada = len(df)
    contadores: dict[str, int] = {}

    # --- T1  Limpiar: espacios sobrantes en todo campo de texto -------------------
    for col in df.columns:
        df[col] = df[col].str.strip()

    # --- T2  Estandarizar estado --------------------------------------------------
    # " PAGADO ", "paid", "Pagado" son el MISMO estado escrito de tres formas.
    estado_original = df["estado"].copy()
    df["estado"] = df["estado"].str.lower().replace(MAPA_ESTADOS)
    contadores["T2_estados_normalizados"] = int((df["estado"] != estado_original).sum())
    contadores["T2_estados_distintos_antes"] = int(estado_original.nunique())
    contadores["T2_estados_distintos_despues"] = int(df["estado"].nunique())

    # --- T3  Estandarizar fecha ---------------------------------------------------
    # El origen usa dos formatos. Se parsea cada uno con su formato EXPLICITO: nunca
    # con un parser que adivine, porque 03/04/2026 es ambiguo y solo el contrato del
    # origen dice que es dd/mm/aaaa.
    es_barra = df["fecha"].str.contains("/", na=False)
    fecha = pd.Series(pd.NaT, index=df.index, dtype="datetime64[ns]")
    fecha[es_barra] = pd.to_datetime(
        df.loc[es_barra, "fecha"], format="%d/%m/%Y", errors="coerce"
    )
    fecha[~es_barra] = pd.to_datetime(
        df.loc[~es_barra, "fecha"], format="%Y-%m-%d", errors="coerce"
    )
    df["fecha"] = fecha
    contadores["T3_fechas_formato_dd_mm_aaaa"] = int(es_barra.sum())
    contadores["T3_fechas_formato_iso"] = int((~es_barra).sum())
    contadores["T3_fechas_no_parseables"] = int(df["fecha"].isna().sum())

    # --- T4  Estandarizar precio --------------------------------------------------
    # "19.990" usa el punto como separador de MILES (convencion chilena), no decimal.
    con_puntos = df["precio_unitario"].str.contains(r"\.", na=False)
    df["precio_unitario"] = pd.to_numeric(
        df["precio_unitario"].str.replace(".", "", regex=False), errors="coerce"
    )
    contadores["T4_precios_con_separador_miles"] = int(con_puntos.sum())

    # --- T5  Estandarizar unidades de peso ----------------------------------------
    en_gramos = df["peso"].str.endswith("g") & ~df["peso"].str.endswith("kg")
    peso_num = pd.to_numeric(
        df["peso"].str.replace(r"\s*(kg|g)$", "", regex=True), errors="coerce"
    )
    df["peso_kg"] = peso_num.where(~en_gramos, peso_num / 1000).round(4)
    df = df.drop(columns=["peso"])
    contadores["T5_pesos_convertidos_de_g_a_kg"] = int(en_gramos.sum())

    # --- T6  Splitting del codigo de pedido ---------------------------------------
    # "SCL-2026-00981" -> sucursal + anio + numero. Separar solo funciona si se conoce
    # la estructura: las filas que no la cumplen se marcan y se CONSERVA el original.
    partes = df["codigo_pedido"].str.extract(
        r"^(?P<sucursal>[A-Z]{3})-(?P<anio_pedido>\d{4})-(?P<numero_pedido>\d+)$"
    )
    df["sucursal"] = partes["sucursal"]
    df["anio_pedido"] = pd.to_numeric(partes["anio_pedido"], errors="coerce").astype("Int64")
    df["numero_pedido"] = partes["numero_pedido"]
    df["codigo_mal_formado"] = partes["sucursal"].isna()
    contadores["T6_codigos_mal_formados"] = int(df["codigo_mal_formado"].sum())

    # --- T7  Deduplicar por clave -------------------------------------------------
    # Misma clave (codigo_pedido, linea) y mismo contenido -> una sola copia.
    # Dos filas con el mismo precio pero CLAVE distinta son dos ventas validas y
    # sobreviven: la deduplicacion es por clave, no por parecido.
    dup_mask = df.duplicated(subset=CLAVE, keep="first")
    contadores["T7_duplicados_por_clave_eliminados"] = int(dup_mask.sum())
    df = df[~dup_mask].copy()

    # --- T8  Cuarentena de filas no interpretables --------------------------------
    # Un valor vacio NO significa cero: asumir cantidad = 0 inventaria una venta de
    # $0 y ensuciaria todos los agregados. Se aisla para revision.
    cantidad = pd.to_numeric(df["cantidad"], errors="coerce")
    invalida = cantidad.isna() | (cantidad <= 0) | df["precio_unitario"].isna() | df["fecha"].isna()
    cuarentena = df[invalida].copy()
    cuarentena["motivo_cuarentena"] = (
        pd.Series("", index=cuarentena.index)
        .mask(pd.to_numeric(cuarentena["cantidad"], errors="coerce").isna(),
              "cantidad vacia o no numerica")
        .mask(cuarentena["precio_unitario"].isna(), "precio no numerico")
        .mask(cuarentena["fecha"].isna(), "fecha no parseable")
    )
    df = df[~invalida].copy()
    df["cantidad"] = cantidad[~invalida].astype("int64")
    df["precio_unitario"] = df["precio_unitario"].astype("int64")
    contadores["T8_filas_en_cuarentena"] = len(cuarentena)

    # --- T9  Derivar el importe ---------------------------------------------------
    # La formula necesita una regla de negocio declarada: importe = cantidad x precio,
    # neto, sin impuestos ni descuentos (no vienen en el origen).
    df["importe"] = df["cantidad"] * df["precio_unitario"]

    # --- T10 Joining con el catalogo ----------------------------------------------
    # LEFT join a proposito: una venta sin match en el catalogo es un hallazgo que hay
    # que reportar, no una fila que deba desaparecer del total de ventas.
    df["producto_id"] = pd.to_numeric(df["producto_id"], errors="coerce").astype("int64")
    antes_join = len(df)
    df = df.merge(
        cat[["producto_id", "nombre", "categoria"]], on="producto_id", how="left",
        validate="many_to_one",   # falla si el catalogo volviera a tener duplicados
    )
    df["sin_catalogo"] = df["categoria"].isna()
    df["categoria"] = df["categoria"].fillna("SIN_CATALOGO")
    df["nombre"] = df["nombre"].fillna("desconocido")
    contadores["T10_filas_antes_del_join"] = antes_join
    contadores["T10_filas_despues_del_join"] = len(df)
    contadores["T10_ventas_sin_match_en_catalogo"] = int(df["sin_catalogo"].sum())

    # --- T11 Proteger el dato sensible --------------------------------------------
    # El analisis necesita AGRUPAR por cliente, no recuperar su correo: se reemplaza
    # por un seudonimo HMAC-SHA256 con clave y el email no se carga al destino.
    # (Hashear con clave != cifrar: aqui es deliberadamente irreversible.)
    df["cliente_seudonimo"] = [
        hmac.new(CLAVE_SEUDONIMO, e.encode(), hashlib.sha256).hexdigest()[:16]
        for e in df["email_cliente"]
    ]
    df = df.drop(columns=["email_cliente"])
    cuarentena = cuarentena.drop(columns=["email_cliente"])
    contadores["T11_emails_seudonimizados"] = len(df)

    # --- Tipos finales ------------------------------------------------------------
    # linea y cliente_id son numericos. numero_pedido se mantiene como TEXTO a
    # proposito: es un identificador con ceros a la izquierda ("00981"), no una
    # cantidad, y convertirlo a entero perderia el formato del codigo de origen.
    df["linea"] = df["linea"].astype("int64")
    df["cliente_id"] = df["cliente_id"].astype("int64")

    # ------------------------------------------------------------------- persistir
    columnas = [
        "codigo_pedido", "linea", "sucursal", "anio_pedido", "numero_pedido",
        "fecha", "cliente_id", "cliente_seudonimo", "producto_id", "nombre",
        "categoria", "cantidad", "precio_unitario", "importe", "peso_kg",
        "estado", "canal", "codigo_mal_formado", "sin_catalogo",
    ]
    df = df[columnas].sort_values(["fecha", "codigo_pedido", "linea"])
    df.to_parquet(F_LIMPIAS, index=False)
    cuarentena.to_csv(F_CUARENTENA, index=False)

    por_estado = df["estado"].value_counts().to_dict()

    yield dg.MaterializeResult(
        asset_key="ventas_limpias",
        metadata={
            "filas_entrada": n_entrada,
            "filas_salida": len(df),
            "importe_total_clp": int(df["importe"].sum()),
            "rango_fechas": f"{df['fecha'].min():%Y-%m-%d} a {df['fecha'].max():%Y-%m-%d}",
            "clientes_distintos": int(df["cliente_seudonimo"].nunique()),
            "transformaciones": dg.MetadataValue.json(contadores),
            "filas_por_estado": dg.MetadataValue.json({k: int(v) for k, v in por_estado.items()}),
            "destino": str(F_LIMPIAS.relative_to(RAIZ)),
            "muestra": _md(df),
        },
    )
    yield dg.MaterializeResult(
        asset_key="ventas_cuarentena",
        metadata={
            "filas": len(cuarentena),
            "motivos": dg.MetadataValue.json(
                {k: int(v) for k, v in cuarentena["motivo_cuarentena"].value_counts().to_dict().items()}
            ),
            "destino": str(F_CUARENTENA.relative_to(RAIZ)),
            "nota": "No se imputan valores: un vacio no es un cero.",
            "muestra": _md(cuarentena[["codigo_pedido", "linea", "cantidad", "motivo_cuarentena"]]),
        },
    )


@dg.asset(
    deps=["ventas_limpias"],
    group_name="transform",
    description="Transform (T12 Resumir): cambia el grano de linea de venta a "
                "categoria x mes. Se gana el total, se pierde el detalle.",
)
def ventas_por_categoria_mes() -> dg.MaterializeResult:
    df = pd.read_parquet(F_LIMPIAS)

    # Solo ventas efectivas: incluir anuladas inflaria el ingreso. Es una decision de
    # negocio, y por eso queda escrita aqui y en la metadata.
    efectivas = df[df["estado"] == "pagado"].copy()
    efectivas["mes"] = efectivas["fecha"].dt.strftime("%Y-%m")

    resumen = (
        efectivas.groupby(["mes", "categoria"], as_index=False)
        .agg(
            n_ventas=("importe", "size"),
            unidades=("cantidad", "sum"),
            importe_total=("importe", "sum"),
            ticket_promedio=("importe", "mean"),
        )
        .sort_values(["mes", "importe_total"], ascending=[True, False])
    )
    resumen["ticket_promedio"] = resumen["ticket_promedio"].round(0).astype("int64")
    resumen.to_csv(F_RESUMEN, index=False)

    top = (
        resumen.groupby("categoria", as_index=False)["importe_total"].sum()
        .sort_values("importe_total", ascending=False)
    )
    return dg.MaterializeResult(
        metadata={
            "filas": len(resumen),
            "meses": int(resumen["mes"].nunique()),
            "categorias": int(resumen["categoria"].nunique()),
            "importe_total_clp": int(resumen["importe_total"].sum()),
            "filtro_aplicado": "solo estado = 'pagado' (se excluyen pendientes y anuladas)",
            "cambio_de_grano": "1 fila por linea de venta -> 1 fila por (mes, categoria)",
            "destino": str(F_RESUMEN.relative_to(RAIZ)),
            "total_por_categoria": _md(top, 10),
            "muestra": _md(resumen),
        }
    )


# ================================================================== LOAD ==========
@dg.asset(
    deps=["ventas_limpias", "ventas_por_categoria_mes"],
    group_name="load",
    description="Load: publica detalle y resumen en una base DuckDB local. La carga "
                "es idempotente y transaccional: repetirla deja el mismo estado final.",
)
def warehouse_ventas() -> dg.MaterializeResult:
    WAREHOUSE.mkdir(parents=True, exist_ok=True)
    detalle = pd.read_parquet(F_LIMPIAS)
    resumen = pd.read_csv(F_RESUMEN)

    con = duckdb.connect(F_DUCKDB)
    try:
        # Idempotencia: CREATE OR REPLACE dentro de una transaccion. Si la carga falla
        # a mitad de camino se revierte completa, y nadie consulta un estado parcial
        # (el problema de la "correccion a medias" de la Clase 01).
        con.execute("BEGIN TRANSACTION")
        con.register("df_detalle", detalle)
        con.register("df_resumen", resumen)
        con.execute("CREATE OR REPLACE TABLE ventas AS SELECT * FROM df_detalle")
        con.execute("CREATE OR REPLACE TABLE ventas_por_categoria_mes AS SELECT * FROM df_resumen")
        con.execute("COMMIT")

        # Validar DESPUES de confirmar: la carga no esta "lista" porque no dio error,
        # sino porque los conteos e importes del destino cuadran con el origen.
        n_ventas = con.execute("SELECT COUNT(*) FROM ventas").fetchone()[0]
        n_resumen = con.execute("SELECT COUNT(*) FROM ventas_por_categoria_mes").fetchone()[0]
        total_dest = con.execute("SELECT SUM(importe) FROM ventas").fetchone()[0]
        top = con.execute(
            "SELECT categoria, SUM(importe) AS importe_total, COUNT(*) AS n_ventas "
            "FROM ventas GROUP BY categoria ORDER BY importe_total DESC"
        ).df()
    finally:
        con.close()

    return dg.MaterializeResult(
        metadata={
            "base_de_datos": str(F_DUCKDB.relative_to(RAIZ)),
            "tabla_ventas_filas": int(n_ventas),
            "tabla_resumen_filas": int(n_resumen),
            "importe_total_cargado_clp": int(total_dest),
            "cuadra_con_origen": bool(
                n_ventas == len(detalle) and int(total_dest) == int(detalle["importe"].sum())
            ),
            "carga": "full / CREATE OR REPLACE en una transaccion (idempotente)",
            "consulta_de_verificacion": _md(top, 10),
        }
    )


# ======================================================== ASSET CHECKS ===========
@dg.asset_check(asset="ventas_limpias",
                description="La clave (codigo_pedido, linea) debe ser unica.")
def claves_unicas() -> dg.AssetCheckResult:
    df = pd.read_parquet(F_LIMPIAS)
    n = int(df.duplicated(subset=CLAVE).sum())
    return dg.AssetCheckResult(passed=n == 0, metadata={"duplicados_encontrados": n})


@dg.asset_check(asset="ventas_limpias",
                description="importe debe ser exactamente cantidad x precio_unitario.")
def importe_coherente() -> dg.AssetCheckResult:
    df = pd.read_parquet(F_LIMPIAS)
    malas = int((df["importe"] != df["cantidad"] * df["precio_unitario"]).sum())
    nulos = int(df[["importe", "cantidad", "precio_unitario"]].isna().sum().sum())
    return dg.AssetCheckResult(
        passed=malas == 0 and nulos == 0,
        metadata={"filas_incoherentes": malas, "valores_nulos": nulos},
    )


@dg.asset_check(asset="ventas_limpias",
                description="estado solo puede ser pagado, pendiente o anulado.")
def estados_normalizados() -> dg.AssetCheckResult:
    df = pd.read_parquet(F_LIMPIAS)
    encontrados = set(df["estado"].unique())
    invalidos = sorted(encontrados - ESTADOS_VALIDOS)
    return dg.AssetCheckResult(
        passed=not invalidos,
        metadata={"estados_encontrados": sorted(encontrados),
                  "estados_invalidos": invalidos},
    )


@dg.asset_check(asset="ventas_limpias",
                description="Ninguna fecha nula y todas dentro del rango esperado.")
def fechas_validas() -> dg.AssetCheckResult:
    df = pd.read_parquet(F_LIMPIAS)
    nulas = int(df["fecha"].isna().sum())
    fuera = int(((df["fecha"] < "2025-01-01") | (df["fecha"] > "2026-12-31")).sum())
    return dg.AssetCheckResult(
        passed=nulas == 0 and fuera == 0,
        metadata={"fechas_nulas": nulas, "fuera_de_rango": fuera,
                  "min": str(df["fecha"].min().date()), "max": str(df["fecha"].max().date())},
    )


@dg.asset_check(
    asset="ventas_limpias",
    description="Cuadre contra la verdad conocida: el ETL debe haber eliminado "
                "exactamente los duplicados plantados y aislado las filas invalidas.",
)
def cuadra_con_manifiesto() -> dg.AssetCheckResult:
    man = json.loads(F_MANIFIESTO.read_text(encoding="utf-8"))
    limpias = pd.read_parquet(F_LIMPIAS)
    cuarentena = pd.read_csv(F_CUARENTENA)

    esperadas = man["filas_validas_esperadas"]
    obtenidas = len(limpias)
    cuar_esperada = man["D3_cantidad_vacia_plantada"]
    return dg.AssetCheckResult(
        passed=obtenidas == esperadas and len(cuarentena) == cuar_esperada,
        metadata={
            "filas_validas_esperadas": esperadas,
            "filas_validas_obtenidas": obtenidas,
            "cuarentena_esperada": cuar_esperada,
            "cuarentena_obtenida": len(cuarentena),
            "duplicados_plantados": man["D1_duplicados_exactos_plantados"],
            "filas_parecidas_que_debian_sobrevivir": man["D2_filas_parecidas_validas_plantadas"],
        },
    )


@dg.asset_check(
    asset="ventas_por_categoria_mes",
    description="El resumen debe cuadrar con el detalle: resumir no puede cambiar el total.",
)
def cuadratura_detalle_resumen() -> dg.AssetCheckResult:
    detalle = pd.read_parquet(F_LIMPIAS)
    resumen = pd.read_csv(F_RESUMEN)
    total_detalle = int(detalle.loc[detalle["estado"] == "pagado", "importe"].sum())
    total_resumen = int(resumen["importe_total"].sum())
    n_detalle = int((detalle["estado"] == "pagado").sum())
    n_resumen = int(resumen["n_ventas"].sum())
    return dg.AssetCheckResult(
        passed=total_detalle == total_resumen and n_detalle == n_resumen,
        metadata={"importe_detalle": total_detalle, "importe_resumen": total_resumen,
                  "ventas_detalle": n_detalle, "ventas_resumen": n_resumen,
                  "diferencia": total_detalle - total_resumen},
    )


@dg.asset_check(
    asset="warehouse_ventas",
    description="Lo cargado en DuckDB debe cuadrar en filas e importe con el Parquet.",
)
def warehouse_cuadra() -> dg.AssetCheckResult:
    detalle = pd.read_parquet(F_LIMPIAS)
    con = duckdb.connect(F_DUCKDB, read_only=True)
    try:
        n, total = con.execute("SELECT COUNT(*), SUM(importe) FROM ventas").fetchone()
        sin_email = "email_cliente" not in [
            c[0] for c in con.execute("DESCRIBE ventas").fetchall()
        ]
    finally:
        con.close()
    return dg.AssetCheckResult(
        passed=int(n) == len(detalle) and int(total) == int(detalle["importe"].sum()) and sin_email,
        metadata={"filas_duckdb": int(n), "filas_parquet": len(detalle),
                  "importe_duckdb": int(total),
                  "importe_parquet": int(detalle["importe"].sum()),
                  "email_no_cargado": sin_email},
    )
