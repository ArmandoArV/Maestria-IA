"""Histogramas de color: 3x1D por canal y 3D RGB (Semana 03)."""

import cv2
import numpy as np

from Functions.histogram import binLimits


def channelHistograms(imageBGR, bins=4, maxValue=256):
    """Histogramas 1D normalizados de cada canal, en orden (R, G, B).

    Cada canal se normaliza por separado, igual que el codigo del curso.
    """
    canales = cv2.split(np.asarray(imageBGR, dtype=np.uint8))
    salida = []
    for canal in reversed(canales):                      # BGR -> RGB
        hist = cv2.calcHist([canal], [0], None, [bins], (0, maxValue)).flatten()
        salida.append(hist / hist.sum())
    return salida


def colorHistogram3D(imageBGR, bins=4, maxValue=256):
    """Histograma 3D normalizado, aplanado en orden (B, G, R) de cv2."""
    hist = cv2.calcHist([np.asarray(imageBGR, dtype=np.uint8)], [0, 1, 2], None,
                        [bins, bins, bins],
                        [0, maxValue, 0, maxValue, 0, maxValue]).flatten()
    return hist / hist.sum()


def binOf(valor, bins=4, maxValue=256):
    """Indice (base 0) del bin al que cae un valor."""
    limites = binLimits(bins, maxValue)
    for i in range(bins):
        if limites[i] <= valor < limites[i + 1]:
            return i
    return bins - 1


def nonZeroBins3D(hist3d, bins=4, maxValue=256):
    """Lista de (binR, binG, binB, rangoR, rangoG, rangoB, altura) no nulos.

    cv2 aplana el histograma en el orden de los canales de la imagen (B, G, R),
    aqui se reordena a (R, G, B) para reportarlo.
    """
    limites = binLimits(bins, maxValue)
    cubo = hist3d.reshape(bins, bins, bins)              # [B][G][R]
    salida = []
    for b in range(bins):
        for g in range(bins):
            for r in range(bins):
                altura = cubo[b][g][r]
                if altura == 0:
                    continue
                rango = lambda i: (limites[i], limites[i + 1] - 1)
                salida.append((r, g, b, rango(r), rango(g), rango(b), float(altura)))
    return sorted(salida, key=lambda t: -t[6])


def printChannelHistograms(histogramas, bins=4, maxValue=256):
    limites = binLimits(bins, maxValue)
    for nombre, hist in zip("RGB", histogramas):
        print("  canal {}:".format(nombre))
        for i, altura in enumerate(hist):
            if altura == 0:
                continue
            print("    bin {} [{:3d}, {:3d}] = {:.4f}".format(
                i + 1, limites[i], limites[i + 1] - 1, altura))
