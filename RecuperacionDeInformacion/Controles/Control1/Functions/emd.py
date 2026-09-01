"""Earth Mover's Distance con ground-distance en CIE LAB (Semana 03 b)."""

import cv2
import numpy as np


def rgbToLab(rgb):
    """Convierte un color RGB de 8 bits a CIE LAB (L en [0,100], a y b reales)."""
    pixel = np.array([[list(rgb)]], dtype=np.float32) / 255.0
    return cv2.cvtColor(pixel, cv2.COLOR_RGB2Lab)[0][0]


def costMatrix(coloresA, coloresB):
    """Matriz de costos: distancia euclidiana en CIE LAB entre cada par."""
    labA = [rgbToLab(c) for c in coloresA]
    labB = [rgbToLab(c) for c in coloresB]
    return np.array([[float(np.linalg.norm(a - b)) for b in labB] for a in labA])


def isValidFlow(flujo, pesosA, pesosB, tol=1e-6):
    """Un flujo es valido si no es negativo y respeta las masas de cada lado."""
    flujo = np.asarray(flujo, dtype=float)
    return (flujo >= -tol).all() \
        and np.allclose(flujo.sum(axis=1), pesosA, atol=tol) \
        and np.allclose(flujo.sum(axis=0), pesosB, atol=tol)


def greedyFlow(pesosA, pesosB):
    """Flujo valido construido de forma golosa (northwest corner).

    No es necesariamente el optimo, pero si una matriz de flujos valida.
    """
    a = list(map(float, pesosA))
    b = list(map(float, pesosB))
    flujo = np.zeros((len(a), len(b)))
    i = j = 0
    while i < len(a) and j < len(b):
        mover = min(a[i], b[j])
        flujo[i][j] = mover
        a[i] -= mover
        b[j] -= mover
        if a[i] <= 1e-12:
            i += 1
        else:
            j += 1
    return flujo


def emd(costos, flujo):
    """EMD = suma(costo * flujo) / suma(flujo)."""
    costos, flujo = np.asarray(costos), np.asarray(flujo)
    return float((costos * flujo).sum() / flujo.sum())


def greedyByCostFlow(pesosA, pesosB, costos):
    """Flujo valido construido llenando primero las celdas mas baratas.

    Es reproducible a mano: se ordenan las celdas por costo y en cada una se
    mueve toda la masa que se pueda. No garantiza el optimo en general, pero
    es mucho mejor que la esquina noroeste porque mira los costos.
    """
    a = list(map(float, pesosA))
    b = list(map(float, pesosB))
    costos = np.asarray(costos)
    flujo = np.zeros(costos.shape)
    celdas = sorted(((costos[i][j], i, j)
                     for i in range(len(a)) for j in range(len(b))))
    for _, i, j in celdas:
        mover = min(a[i], b[j])
        if mover <= 1e-12:
            continue
        flujo[i][j] = mover
        a[i] -= mover
        b[j] -= mover
    return flujo
