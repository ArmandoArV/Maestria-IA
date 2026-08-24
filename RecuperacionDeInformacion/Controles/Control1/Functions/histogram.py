import numpy as np


def binLimits(bins, maxValue=256):
    """Divide [0, maxValue) en `bins` tramos. binLimits(2) -> [0, 128, 256]"""
    limites = [round(maxValue * i / bins) for i in range(bins)]
    limites.append(maxValue)
    return limites


def normalizedHistogram(image, bins=256, maxValue=256):
    """Histograma normalizado de una imagen (o de una zona)."""
    valores = np.asarray(image, dtype=np.float32).reshape(-1)
    limites = binLimits(bins, maxValue)
    conteo = np.zeros(bins)
    for valor in valores:
        for b in range(bins):
            if limites[b] <= valor < limites[b + 1]:
                conteo[b] += 1
                break
    total = conteo.sum()
    return conteo / total if total else conteo


def zoneLimits(size, zones):
    return [round(size * i / zones) for i in range(zones)] + [size]


def histogramByZones(image, zonesX=2, zonesY=2, bins=256, maxValue=256):
    """Un histograma normalizado independiente por zona.

    Devuelve una lista de (fila_zona, columna_zona, histograma).
    """
    imagen = np.asarray(image, dtype=np.float32)
    limites_y = zoneLimits(imagen.shape[0], zonesY)
    limites_x = zoneLimits(imagen.shape[1], zonesX)
    resultado = []
    for j in range(zonesY):
        for i in range(zonesX):
            zona = imagen[limites_y[j]:limites_y[j + 1], limites_x[i]:limites_x[i + 1]]
            resultado.append((j, i, normalizedHistogram(zona, bins, maxValue)))
    return resultado


def printHistogram(histogram, bins=None, maxValue=256, onlyNonZero=True):
    """Imprime el histograma indicando qué rango representa cada bin y su altura."""
    histogram = np.asarray(histogram)
    bins = len(histogram) if bins is None else bins
    limites = binLimits(bins, maxValue)
    for b in range(bins):
        if onlyNonZero and histogram[b] == 0:
            continue
        print("  bin {:>3} [{:>3}, {:>3}] = {:.4f}".format(
            b + 1, limites[b], limites[b + 1] - 1, histogram[b]))
