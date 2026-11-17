# Actividad 2: ETL y Orquestación (INF3862)

ETL de ventas construido y ejecutado con **Dagster**.

## Archivos de esta carpeta

| Archivo | Qué es |
|---|---|
| `crear_dataset.py` | Paso 1: genera el dataset de origen con suciedad plantada en cantidades conocidas |
| `etl_ventas_assets.py` | **El ETL**: 6 assets (extract → transform → load) + 7 asset checks |
| `parte_teorica.md` | Respuestas a las tres preguntas teóricas |
| `01_run_exitosa_gantt.png` | **Run exitosa**: 6 assets, 7 checks, 12 steps, 0 errores |
| `02_lineage_assets.png` | Grafo de activos materializados (extract / transform / load) |
| `03_metadata_ventas_limpias.png` | Metadata de la transformación (2.043 → 1.978 filas, contadores por técnica) |
| `04_asset_checks.png` | Los 5 asset checks de `ventas_limpias`, todos en verde |

> `etl_ventas_assets.py` es una copia de `src/etl_ventas/defs/assets.py` del proyecto Dagster,
> renombrada para que se entienda fuera del proyecto.

## Cómo reproducirlo

```bash
uvx create-dagster@latest project --uv-sync etl-ventas
cd etl-ventas && uv add pandas duckdb pyarrow
# copiar crear_dataset.py a la raíz y assets.py a src/etl_ventas/defs/
python crear_dataset.py          # genera data/raw/
dg dev                           # http://localhost:3000 -> Assets -> Materialize all
```

## El pipeline

```
ventas_crudas ────────────┐
                          ├──> ventas_limpias ──> ventas_por_categoria_mes ──┐
catalogo_productos ───────┘         │                                        │
                                    └──> ventas_cuarentena                   │
                                                                             │
                          warehouse_ventas (DuckDB local) <──────────────────┘
```

**Técnicas de transformación aplicadas (Clase 02):** limpiar · estandarizar (fecha, precio,
unidades, estado) · derivar · joining con control de cardinalidad · splitting · deduplicar ·
resumir (cambio de grano) · proteger dato sensible.

## Resultado medido

| | |
|---|---:|
| Filas de entrada | 2.043 |
| Duplicados por clave eliminados | 40 |
| Filas enviadas a cuarentena | 25 |
| **Filas válidas de salida** | **1.978** |
| Estados distintos: antes → después | 10 → 3 |
| Fechas normalizadas (dd/mm/aaaa + ISO) | 966 + 1.077 |
| Precios con separador de miles corregidos | 840 |
| Pesos convertidos de g a kg | 602 |
| Ventas sin match en el catálogo (conservadas y marcadas) | 18 |
| Importe total cargado a DuckDB | $285.501.140 |

Los 7 asset checks pasan, incluido el cuadre contra el manifiesto de suciedad plantada
(`filas_validas_esperadas` = `filas_validas_obtenidas` = 1.978) y el cuadre detalle-vs-resumen.
