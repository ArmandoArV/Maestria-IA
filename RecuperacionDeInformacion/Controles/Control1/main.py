"""
    Hecho por: armando arredondo valle
    Control 1 - INF3841 Recuperación de Información
    Semana 01 y Semana 02
"""

import os

import cv2
import numpy as np

from Classes.Matrix import Matrix
from Functions.gradient import gradient, gradientAngle, gradientMagnitude
from Functions.histogram import histogramByZones, normalizedHistogram, printHistogram
from Functions.hog import anglesByZone, hog, printAngleHistogram
from Functions.kernels import SOBEL_X, SOBEL_Y
from Functions.medianFilter import medianFilter
from Functions.padToSize import padToSize
from Functions.plots import (plotAngleHistogram, plotHistogram, plotHistogramsByZones,
                             plotHOGByZones)
from Functions.threshold import threshold
from Functions.validateConvolution import validateConvolution

# si es True guarda los gráficos como PNG en graficos/; si es False los muestra en pantalla
GUARDAR_GRAFICOS = True
# los gráficos se guardan dentro de Informe/ para que el .tex los encuentre
CARPETA_GRAFICOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Informe", "graficos")


def archivo(nombre):
    """Ruta donde guardar un gráfico (o None para mostrarlo en pantalla)."""
    if not GUARDAR_GRAFICOS:
        return None
    os.makedirs(CARPETA_GRAFICOS, exist_ok=True)
    return os.path.join(CARPETA_GRAFICOS, nombre)


# =====================================================================
# SEMANA 01 - a)  imagen A de 5x5
# =====================================================================
A = Matrix(np.array([[200,  50, 200,  50,  50],
                     [ 50, 200,  50,  50,  50],
                     [200,  50, 200,  50, 200],
                     [ 50,  50,  50, 200,  50],
                     [ 50,  50, 200,  50, 200]], dtype=np.float32))

K = Matrix(np.array([[ 1, -2,  1],
                     [-2,  4, -2],
                     [ 1, -2,  1]], dtype=np.float32))

print("Matriz A:")
print(A)
print("\nMatriz K:")
print(K)

#  a) i.  A * K  (K es simétrica, así que da igual reflejarla o no)
A_K = validateConvolution(A, K, reflect_kernel=True)
print("\na) i.  A * K  (sólo donde el kernel cabe completo, profundidad 32f):")
print(padToSize(A_K, (A.rows, A.cols)))

# verificación independiente con OpenCV
margen = K.rows // 2
opencv = cv2.filter2D(A.to_array(np.float32), ddepth=cv2.CV_32F,
                      kernel=K.to_array(np.float32))[margen:-margen, margen:-margen]
print("   (¿coincide con cv2.filter2D()?", np.allclose(A_K, opencv), ")")

#  a) ii.  umbral U_t con t=1000 sobre A * K
print("\na) ii.  U_t(A * K) con t=1000:")
print(padToSize(threshold(A_K, t=1000), (A.rows, A.cols)))

#  a) iii.  filtro de mediana 3x3 sobre A
print("\na) iii.  mediana 3x3 de A:")
print(padToSize(medianFilter(A, 3), (A.rows, A.cols)))

# SEMANA 01 - b)  imagen B de 7x7

B = Matrix(np.array([[255, 255, 255, 255, 127, 127, 127],
                 [255, 255, 255, 127, 127, 127, 127],
                 [255, 255, 127, 127, 127, 127, 127],
                 [255, 127, 127, 127, 127, 127,   0],
                 [127, 127, 127, 127, 127,   0,   0],
                 [127, 127, 127, 127,   0,   0,   0],
                 [127, 127, 127,   0,   0,   0,   0]], dtype=np.float32))


if B is not None:
    B = B if isinstance(B, Matrix) else Matrix(B)
    Bx, By = gradient(B)          # usa Sobel y reflect_kernel=True (convolución real)

    print("\nb) i.  Bx = B * Sx:")
    print(padToSize(Bx, (B.rows, B.cols)))

    print("\nb) ii.  By = B * Sy:")
    print(padToSize(By, (B.rows, B.cols)))

    print("\nb) iii.  magnitud del gradiente:")
    print(padToSize(gradientMagnitude(Bx, By), (B.rows, B.cols)).display(decimal_places=1))

    print("\nb) iv.  ángulo del gradiente en [-180, 180]:")
    print(padToSize(gradientAngle(Bx, By), (B.rows, B.cols)).display(decimal_places=1))

# SEMANA 02 - imagen I de 8x8
I = Matrix(np.array([[127, 127, 127, 127,   0, 255,   0, 255],
                 [  0, 127, 127, 127, 255,   0, 255,   0],
                 [  0,   0, 127, 127,   0, 255,   0, 255],
                 [  0,   0,   0, 127, 255,   0, 255,   0],
                 [255, 255, 255, 255, 127, 127, 255, 255],
                 [255, 255, 255, 255, 127, 127, 255, 255],
                 [  0,   0,   0,   0, 127, 127, 255, 255],
                 [  0,   0,   0,   0, 127, 127, 255, 255]], 
dtype=np.float32))

if I is not None:
    I = I if isinstance(I, Matrix) else Matrix(I)

    #  i.  histograma global normalizado de 256 bins
    print("\nSemana 02 - i.  histograma global de 256 bins (bins distintos de cero):")
    histograma_global = normalizedHistogram(I, bins=256)
    printHistogram(histograma_global)
    plotHistogram(histograma_global, "Histograma de grises de I",
                  savePath=archivo("semana02-i-histograma-global.png"))

    #  ii.  histograma de 256 bins por zonas 2x2
    print("\nSemana 02 - ii.  histograma de 256 bins en 2x2 zonas:")
    zonas = histogramByZones(I, zonesX=2, zonesY=2, bins=256)
    for fila, columna, histograma in zonas:
        print(" zona (fila {}, columna {}):".format(fila + 1, columna + 1))
        printHistogram(histograma)
    plotHistogramsByZones(zonas, "Histograma de grises de I en 2x2 zonas",
                          savePath=archivo("semana02-ii-histograma-zonas.png"))

    #  iii.  HOG 2x2 zonas, 9 bins en (-90, 90], magnitud >= 200, división estricta
    print("\nSemana 02 - iii.  HOG 2x2 zonas x 9 bins en (-90, 90]:")
    angulos = anglesByZone(I, zonesX=2, zonesY=2, minMagnitude=200,
                           range180=False, strict=True)
    histogramas = hog(I, zonesX=2, zonesY=2, bins=9, minMagnitude=200,
                      range180=False, strict=True)
    for (fila, columna, angs), (_, _, histograma) in zip(angulos, histogramas):
        print(" zona (fila {}, columna {}) - ángulos de borde: {}".format(
            fila + 1, columna + 1, [round(a, 1) for a in angs]))
        printAngleHistogram(histograma)
    plotHOGByZones(histogramas, "HOG de I en 2x2 zonas (9 bins en (-90, 90])",
                   savePath=archivo("semana02-iii-hog-zonas.png"))
