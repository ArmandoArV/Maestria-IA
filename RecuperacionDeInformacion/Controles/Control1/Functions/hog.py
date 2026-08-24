"""
HOG - Histogram of Oriented Gradients (Slides 02.3).

Pasos:
  1. Sobel -> Ix, Iy
  2. magnitud = sqrt(Ix^2 + Iy^2); sólo se consideran los pixeles con magnitud >= minMagnitude
  3. ángulo = atan2(Iy, Ix), llevado al rango pedido
  4. un histograma normalizado de `bins` por zona

`strict=True` calcula el gradiente DENTRO de cada zona, es decir, no usa pixeles de las
zonas vecinas (es la división estricta de zonas).
"""

import numpy as np

from Functions.gradient import gradient, gradientAngle, gradientMagnitude
from Functions.histogram import zoneLimits


def angleBinLimits(bins, range180=False):
    desde, hasta = (-180.0, 180.0) if range180 else (-90.0, 90.0)
    return np.linspace(desde, hasta, bins + 1)


def angleHistogram(angles, bins=9, range180=False):
    """Histograma normalizado de una lista de ángulos. El bin b cubre (limite_b, limite_b+1]."""
    limites = angleBinLimits(bins, range180)
    conteo = np.zeros(bins)
    for angulo in angles:
        for b in range(bins):
            if limites[b] < angulo <= limites[b + 1] or (b == 0 and angulo == limites[0]):
                conteo[b] += 1
                break
    total = conteo.sum()
    return conteo / total if total else conteo


def anglesByZone(image, zonesX=2, zonesY=2, minMagnitude=200, range180=False, strict=True):
    """Ángulos de los pixeles de borde de cada zona: lista de (fila, columna, angulos)."""
    imagen = np.asarray(image, dtype=np.float32)
    limites_y = zoneLimits(imagen.shape[0], zonesY)
    limites_x = zoneLimits(imagen.shape[1], zonesX)
    resultado = []
    if not strict:
        ix, iy = gradient(imagen)
        magnitud_total = gradientMagnitude(ix, iy)
        angulos_total = gradientAngle(ix, iy, range180)
    for j in range(zonesY):
        for i in range(zonesX):
            if strict:
                zona = imagen[limites_y[j]:limites_y[j + 1], limites_x[i]:limites_x[i + 1]]
                ix, iy = gradient(zona)
                magnitud = gradientMagnitude(ix, iy)
                angulos = gradientAngle(ix, iy, range180)
            else:
                # el gradiente válido está desplazado 1 pixel respecto de la imagen
                magnitud = magnitud_total[limites_y[j]:limites_y[j + 1] - 2,
                                          limites_x[i]:limites_x[i + 1] - 2]
                angulos = angulos_total[limites_y[j]:limites_y[j + 1] - 2,
                                        limites_x[i]:limites_x[i + 1] - 2]
            mascara = (magnitud >= minMagnitude) & ~np.isnan(angulos)
            resultado.append((j, i, angulos[mascara].tolist()))
    return resultado


def hog(image, zonesX=2, zonesY=2, bins=9, minMagnitude=200, range180=False, strict=True):
    """Devuelve una lista de (fila_zona, columna_zona, histograma_de_angulos)."""
    return [(j, i, angleHistogram(angulos, bins, range180))
            for j, i, angulos in anglesByZone(image, zonesX, zonesY, minMagnitude,
                                              range180, strict)]


def printAngleHistogram(histogram, range180=False):
    """Imprime el histograma indicando el rango de ángulos de cada bin y su altura."""
    histogram = np.asarray(histogram)
    limites = angleBinLimits(len(histogram), range180)
    for b in range(len(histogram)):
        print("  bin {:>2} ({:>6.1f}, {:>6.1f}] = {:.4f}".format(
            b + 1, limites[b], limites[b + 1], histogram[b]))
