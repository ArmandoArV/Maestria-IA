"""
Actividad 2 - INF3862 | Paso 1: crear el dataset de origen.

Genera dos archivos locales que simulan las fuentes operacionales de una tienda:

    data/raw/ventas_crudas.csv       lineas de venta "sucias", como llegan del origen
    data/raw/catalogo_productos.csv  catalogo de productos (con un defecto a proposito)
    data/raw/_manifiesto_suciedad.json  cuanta suciedad se planto, para verificar el ETL

La suciedad NO es aleatoria: se planta en cantidades conocidas y se deja registrada en el
manifiesto. Asi el pipeline puede verificarse contra la verdad conocida ("plante 40
duplicados exactos; el ETL elimino 40") en vez de confiar en que la tarea termino en verde.

Cada defecto plantado corresponde a una tecnica de transformacion de la Clase 02:

    D1  duplicados exactos                 -> deduplicar
    D2  filas parecidas pero NO duplicadas -> deduplicar (el caso que NO se debe tocar)
    D3  cantidad vacia                     -> limpiar / marcar para revision
    D4  dos formatos de fecha              -> estandarizar
    D5  separador de miles en el precio    -> estandarizar
    D6  estados en distintos idiomas/casos -> limpiar y estandarizar
    D7  peso en kg y en g                  -> estandarizar unidades
    D8  producto sin match en el catalogo  -> join (que hacer sin coincidencia)
    D9  codigo de pedido mal formado       -> splitting (que hacer si falta una parte)
    D10 producto_id duplicado en catalogo  -> join (cardinalidad: duplicaria la venta)

Uso:  python crear_dataset.py
"""

from __future__ import annotations

import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

SEMILLA = 3862
RAW = Path(__file__).parent / "data" / "raw"

N_BASE = 1_200          # lineas de venta "base"
N_DUP_EXACTOS = 40      # D1
N_PARECIDAS = 15        # D2
N_CANTIDAD_VACIA = 25   # D3
N_SIN_CATALOGO = 18     # D8
N_CODIGO_ROTO = 10      # D9

SUCURSALES = ["SCL", "VAP", "CCP", "ANF", "PMC"]
CANALES = ["web", "tienda", "app", "telefono"]
# D6: el mismo estado escrito de seis maneras distintas
ESTADOS_SUCIOS = {
    "pagado": [" PAGADO ", "paid", "pagado", "Pagado"],
    "pendiente": ["PENDIENTE", "pendiente ", "Pendiente"],
    "anulado": ["ANULADO", "anulado", "cancelled"],
}
CATALOGO = [
    (101, "Notebook 14 pulgadas", "Tecnologia", 649_990, 1.4),
    (102, "Mouse inalambrico", "Tecnologia", 15_990, 0.09),
    (103, "Teclado mecanico", "Tecnologia", 89_990, 0.85),
    (201, "Polera algodon", "Vestuario", 12_990, 0.18),
    (202, "Zapatillas running", "Vestuario", 79_990, 0.62),
    (203, "Chaqueta cortaviento", "Vestuario", 54_990, 0.45),
    (301, "Cafe grano 1kg", "Alimentos", 11_490, 1.0),
    (302, "Aceite oliva 500ml", "Alimentos", 8_990, 0.5),
    (401, "Sarten antiadherente", "Hogar", 24_990, 0.95),
    (402, "Juego de sabanas", "Hogar", 39_990, 1.2),
    (501, "Pelota de futbol", "Deportes", 19_990, 0.43),
    (502, "Mancuernas 5kg par", "Deportes", 34_990, 10.0),
]
PRECIO = {pid: precio for pid, _, _, precio, _ in CATALOGO}
PESO_KG = {pid: peso for pid, _, _, _, peso in CATALOGO}

COLUMNAS = [
    "codigo_pedido", "linea", "fecha", "cliente_id", "email_cliente",
    "producto_id", "cantidad", "precio_unitario", "estado", "peso", "canal",
]


def fmt_fecha(d: date, iso: bool) -> str:
    """D4: la mitad de las filas llega en ISO y la mitad en dd/mm/aaaa."""
    return d.isoformat() if iso else f"{d.day:02d}/{d.month:02d}/{d.year}"


def fmt_precio(valor: int, con_puntos: bool) -> str:
    """D5: el origen a veces usa '.' como separador de miles."""
    return f"{valor:,}".replace(",", ".") if con_puntos else str(valor)


def fmt_peso(kg: float, en_gramos: bool) -> str:
    """D7: el mismo peso expresado en dos unidades distintas."""
    return f"{int(round(kg * 1000))} g" if en_gramos else f"{kg:g} kg"


def main() -> None:
    rnd = random.Random(SEMILLA)
    RAW.mkdir(parents=True, exist_ok=True)
    inicio = date(2025, 1, 1)
    filas: list[dict] = []
    n_pedido = 0

    # ---------------------------------------------------------------- base limpia
    for _ in range(N_BASE):
        n_pedido += 1
        suc = rnd.choice(SUCURSALES)
        dia = inicio + timedelta(days=rnd.randint(0, 699))
        cliente = rnd.randint(1, 300)
        for linea in range(1, rnd.choice([1, 1, 1, 2, 2, 3]) + 1):
            pid = rnd.choice(list(PRECIO))
            estado_limpio = rnd.choices(
                ["pagado", "pendiente", "anulado"], weights=[80, 15, 5]
            )[0]
            filas.append({
                "codigo_pedido": f"{suc}-{dia.year}-{n_pedido:05d}",
                "linea": linea,
                "fecha": fmt_fecha(dia, rnd.random() < 0.5),
                "cliente_id": cliente,
                "email_cliente": f"cliente{cliente:03d}@correo.cl",
                "producto_id": pid,
                "cantidad": rnd.choices([1, 2, 3, 4], weights=[60, 25, 10, 5])[0],
                "precio_unitario": fmt_precio(PRECIO[pid], rnd.random() < 0.4),
                "estado": rnd.choice(ESTADOS_SUCIOS[estado_limpio]),
                "peso": fmt_peso(PESO_KG[pid], rnd.random() < 0.3),
                "canal": rnd.choice(CANALES),
            })

    n_base_filas = len(filas)

    # El orden importa: primero se ensucian las filas base y DESPUES se duplican.
    # Si se duplicara antes, una mutacion posterior podria caer sobre una sola copia
    # del par y el duplicado dejaria de ser exacto -> el manifiesto mentiria.

    # ------------------------------------------------------ D3: cantidad vacia
    idx_vacias = set(rnd.sample(range(n_base_filas), N_CANTIDAD_VACIA))
    for i in idx_vacias:
        filas[i]["cantidad"] = ""

    # ------------------------------------------- D8: producto fuera del catalogo
    for i in rnd.sample(range(n_base_filas), N_SIN_CATALOGO):
        filas[i]["producto_id"] = 999
        filas[i]["precio_unitario"] = fmt_precio(9_990, False)

    # ------------------------------------------- D9: codigo de pedido mal formado
    for i in rnd.sample(range(n_base_filas), N_CODIGO_ROTO):
        # se perdieron la sucursal y el anio: queda solo el numero de pedido
        filas[i]["codigo_pedido"] = filas[i]["codigo_pedido"].split("-")[-1]

    # ------------------------------------------------- D1: duplicados exactos
    # Copia verbatim de filas ya existentes: misma clave (codigo_pedido, linea) y
    # mismo contenido -> se conserva UNA sola copia.
    duplicados = [dict(f) for f in rnd.sample(filas[:n_base_filas], N_DUP_EXACTOS)]
    filas.extend(duplicados)

    # --------------------- D2: filas PARECIDAS pero con clave distinta (validas)
    # Mismo cliente, misma fecha, mismo producto y mismo precio... pero otra linea
    # del pedido. Son dos ventas reales: el ETL NO debe eliminarlas.
    # Se eligen solo entre filas con cantidad valida para que sobrevivan al filtro.
    candidatas = [i for i in range(n_base_filas) if i not in idx_vacias]
    for i in rnd.sample(candidatas, N_PARECIDAS):
        gemela = dict(filas[i])
        gemela["linea"] = int(gemela["linea"]) + 90   # clave distinta, contenido igual
        filas.append(gemela)

    rnd.shuffle(filas)

    with (RAW / "ventas_crudas.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNAS)
        w.writeheader()
        w.writerows(filas)

    # ------------------------------------ catalogo, con D10: producto_id repetido
    cat_filas = [
        {"producto_id": pid, "nombre": nom, "categoria": cat, "precio_lista": pr}
        for pid, nom, cat, pr, _ in CATALOGO
    ]
    # El producto 102 aparece dos veces (precio desactualizado en una de las filas).
    # Si se hace el JOIN sin controlar cardinalidad, CADA venta del 102 se duplica.
    cat_filas.append({"producto_id": 102, "nombre": "Mouse inalambrico",
                      "categoria": "Tecnologia", "precio_lista": 14_990})
    cat_filas.append({"producto_id": 301, "nombre": "Cafe grano 1kg",
                      "categoria": "Alimentos", "precio_lista": 11_490})

    with (RAW / "catalogo_productos.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["producto_id", "nombre", "categoria", "precio_lista"])
        w.writeheader()
        w.writerows(cat_filas)

    # ------------------------------------------------------------- manifiesto
    manifiesto = {
        "semilla": SEMILLA,
        "filas_totales": len(filas),
        "filas_base": n_base_filas,
        "D1_duplicados_exactos_plantados": N_DUP_EXACTOS,
        "D2_filas_parecidas_validas_plantadas": N_PARECIDAS,
        "D3_cantidad_vacia_plantada": N_CANTIDAD_VACIA,
        "D8_sin_catalogo_plantadas": N_SIN_CATALOGO,
        "D9_codigo_mal_formado_plantadas": N_CODIGO_ROTO,
        "D10_productos_duplicados_en_catalogo": 2,
        "filas_validas_esperadas": len(filas) - N_DUP_EXACTOS - N_CANTIDAD_VACIA,
    }
    (RAW / "_manifiesto_suciedad.json").write_text(
        json.dumps(manifiesto, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"ventas_crudas.csv       {len(filas):>6,} filas")
    print(f"catalogo_productos.csv  {len(cat_filas):>6,} filas "
          f"({len(CATALOGO)} productos + 2 duplicados a proposito)")
    print("\nSuciedad plantada:")
    for k, v in manifiesto.items():
        if k.startswith("D"):
            print(f"  {k:<42} {v:>5}")
    print(f"\n  filas validas esperadas tras el ETL      {manifiesto['filas_validas_esperadas']:>5}")


if __name__ == "__main__":
    main()
