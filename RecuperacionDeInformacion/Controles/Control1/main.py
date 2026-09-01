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
from Functions.audio import describePCM, nyquist, pcmSize
from Functions.colorHistogram import (
    channelHistograms,
    colorHistogram3D,
    nonZeroBins3D,
    printChannelHistograms,
)
from Functions.emd import costMatrix, emd, greedyByCostFlow, isValidFlow, rgbToLab
from Functions.histogram import histogramByZones, normalizedHistogram, printHistogram
from Functions.hog import anglesByZone, hog, printAngleHistogram
from Functions.kernels import SOBEL_X, SOBEL_Y
from Functions.medianFilter import medianFilter
from Functions.padToSize import padToSize
from Functions.plots import (
    plotAngleHistogram,
    plotChannelHistograms,
    plotHistogram,
    plotHistogramsByZones,
    plotHOGByZones,
)
from Functions.threshold import threshold
from Functions.validateConvolution import validateConvolution

# si es True guarda los gráficos como PNG en graficos/; si es False los muestra en pantalla
GUARDAR_GRAFICOS = True
# los gráficos se guardan dentro de Informe/ para que el .tex los encuentre
CARPETA_GRAFICOS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "Informe", "graficos"
)


def archivo(nombre):
    """Ruta donde guardar un gráfico (o None para mostrarlo en pantalla)."""
    if not GUARDAR_GRAFICOS:
        return None
    os.makedirs(CARPETA_GRAFICOS, exist_ok=True)
    return os.path.join(CARPETA_GRAFICOS, nombre)


# =====================================================================
# SEMANA 01 - a)  imagen A de 5x5
# =====================================================================
A = Matrix(
    np.array(
        [
            [200, 50, 200, 50, 50],
            [50, 200, 50, 50, 50],
            [200, 50, 200, 50, 200],
            [50, 50, 50, 200, 50],
            [50, 50, 200, 50, 200],
        ],
        dtype=np.float32,
    )
)

K = Matrix(np.array([[1, -2, 1], [-2, 4, -2], [1, -2, 1]], dtype=np.float32))

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
opencv = cv2.filter2D(
    A.to_array(np.float32), ddepth=cv2.CV_32F, kernel=K.to_array(np.float32)
)[margen:-margen, margen:-margen]
print("   (¿coincide con cv2.filter2D()?", np.allclose(A_K, opencv), ")")

#  a) ii.  umbral U_t con t=1000 sobre A * K
print("\na) ii.  U_t(A * K) con t=1000:")
print(padToSize(threshold(A_K, t=1000), (A.rows, A.cols)))

#  a) iii.  filtro de mediana 3x3 sobre A
print("\na) iii.  mediana 3x3 de A:")
print(padToSize(medianFilter(A, 3), (A.rows, A.cols)))

# SEMANA 01 - b)  imagen B de 7x7

B = Matrix(
    np.array(
        [
            [255, 255, 255, 255, 127, 127, 127],
            [255, 255, 255, 127, 127, 127, 127],
            [255, 255, 127, 127, 127, 127, 127],
            [255, 127, 127, 127, 127, 127, 0],
            [127, 127, 127, 127, 127, 0, 0],
            [127, 127, 127, 127, 0, 0, 0],
            [127, 127, 127, 0, 0, 0, 0],
        ],
        dtype=np.float32,
    )
)


if B is not None:
    B = B if isinstance(B, Matrix) else Matrix(B)
    Bx, By = gradient(B)  # usa Sobel por correlación, igual que cv2.Sobel()

    print("\nb) i.  Bx = B * Sx:")
    print(padToSize(Bx, (B.rows, B.cols)))

    print("\nb) ii.  By = B * Sy:")
    print(padToSize(By, (B.rows, B.cols)))

    print("\nb) iii.  magnitud del gradiente:")
    print(
        padToSize(gradientMagnitude(Bx, By), (B.rows, B.cols)).display(decimal_places=1)
    )

    print("\nb) iv.  ángulo del gradiente en [-180, 180]:")
    print(padToSize(gradientAngle(Bx, By), (B.rows, B.cols)).display(decimal_places=1))

# SEMANA 02 - imagen I de 8x8
I = Matrix(
    np.array(
        [
            [127, 127, 127, 127, 0, 255, 0, 255],
            [0, 127, 127, 127, 255, 0, 255, 0],
            [0, 0, 127, 127, 0, 255, 0, 255],
            [0, 0, 0, 127, 255, 0, 255, 0],
            [255, 255, 255, 255, 127, 127, 255, 255],
            [255, 255, 255, 255, 127, 127, 255, 255],
            [0, 0, 0, 0, 127, 127, 255, 255],
            [0, 0, 0, 0, 127, 127, 255, 255],
        ],
        dtype=np.float32,
    )
)

if I is not None:
    I = I if isinstance(I, Matrix) else Matrix(I)

    #  i.  histograma global normalizado de 256 bins
    print("\nSemana 02 - i.  histograma global de 256 bins (bins distintos de cero):")
    histograma_global = normalizedHistogram(I, bins=256)
    printHistogram(histograma_global)
    plotHistogram(
        histograma_global,
        "Histograma de grises de I",
        savePath=archivo("semana02-i-histograma-global.png"),
    )

    #  ii.  histograma de 256 bins por zonas 2x2
    print("\nSemana 02 - ii.  histograma de 256 bins en 2x2 zonas:")
    zonas = histogramByZones(I, zonesX=2, zonesY=2, bins=256)
    for fila, columna, histograma in zonas:
        print(" zona (fila {}, columna {}):".format(fila + 1, columna + 1))
        printHistogram(histograma)
    plotHistogramsByZones(
        zonas,
        "Histograma de grises de I en 2x2 zonas",
        savePath=archivo("semana02-ii-histograma-zonas.png"),
    )

    #  iii.  HOG 2x2 zonas, 9 bins en (-90, 90], magnitud >= 200, división estricta
    print("\nSemana 02 - iii.  HOG 2x2 zonas x 9 bins en (-90, 90]:")
    angulos = anglesByZone(
        I, zonesX=2, zonesY=2, minMagnitude=200, range180=False, strict=True
    )
    histogramas = hog(
        I, zonesX=2, zonesY=2, bins=9, minMagnitude=200, range180=False, strict=True
    )
    for (fila, columna, angs), (_, _, histograma) in zip(angulos, histogramas):
        print(
            " zona (fila {}, columna {}) - ángulos de borde: {}".format(
                fila + 1, columna + 1, [round(a, 1) for a in angs]
            )
        )
        printAngleHistogram(histograma)
    plotHOGByZones(
        histogramas,
        "HOG de I en 2x2 zonas (9 bins en (-90, 90])",
        savePath=archivo("semana02-iii-hog-zonas.png"),
    )


# =====================================================================
# SEMANA 03 - a)  imagen D de 9x6 en color RGB (bandera de Chile)
# =====================================================================
AZUL = (0, 50, 160)
BLANCO = (255, 255, 255)
ROJO = (218, 41, 28)

D = np.zeros((6, 9, 3), dtype=np.uint8)
D[:, :] = BLANCO[::-1]  # cv2 trabaja en BGR
D[0:3, 0:3] = AZUL[::-1]  # canton azul de 3x3
D[1, 1] = BLANCO[::-1]  # la estrella
D[3:6, :] = ROJO[::-1]  # mitad inferior roja

print("\n" + "=" * 60)
print("SEMANA 03 - a)  imagen D de 9x6 (RGB 24 bits)")
for color, nombre in [(AZUL, "azul"), (BLANCO, "blanco"), (ROJO, "rojo")]:
    print(
        "  {:6s} RGB{}: {} pixeles".format(
            nombre, color, int((D == np.array(color[::-1])).all(axis=2).sum())
        )
    )

#  i.  histograma global normalizado por canal 4+4+4
print("\nSemana 03 - a) i.  histograma por canal 4+4+4:")
canales = channelHistograms(D, bins=4)
printChannelHistograms(canales, bins=4)
plotChannelHistograms(
    canales,
    "Histograma por canal 4+4+4 de D",
    bins=4,
    savePath=archivo("semana03-i-histograma-canales.png"),
)

#  ii.  histograma 3D RGB 4x4x4 normalizado
print("\nSemana 03 - a) ii.  histograma 3D RGB 4x4x4 (bins distintos de cero):")
hist3d = colorHistogram3D(D, bins=4)
for r, g, b, rr, rg, rb, altura in nonZeroBins3D(hist3d, bins=4):
    print(
        "  bin (R{}, G{}, B{}) = R[{:3d},{:3d}] G[{:3d},{:3d}] B[{:3d},{:3d}] -> {:.4f}".format(
            r + 1, g + 1, b + 1, rr[0], rr[1], rg[0], rg[1], rb[0], rb[1], altura
        )
    )
print(
    "  suma = {:.4f}   (bins no nulos: {} de {})".format(
        hist3d.sum(), int((hist3d > 0).sum()), hist3d.size
    )
)

# =====================================================================
# SEMANA 03 - b)  Earth Mover's Distance entre dos histogramas de color
# =====================================================================
COLORES_1 = [(85, 137, 184), (211, 56, 69), (19, 34, 103)]
PESOS_1 = [0.55, 0.30, 0.15]
COLORES_2 = [(233, 47, 36), (15, 42, 162), (140, 211, 247)]
PESOS_2 = [0.25, 0.50, 0.25]

print("\n" + "=" * 60)
print("SEMANA 03 - b)  EMD entre los histogramas 1 y 2")

print("\n  colores en CIE LAB:")
for nombre, colores in [("histograma 1", COLORES_1), ("histograma 2", COLORES_2)]:
    for i, color in enumerate(colores):
        L, a, b = rgbToLab(color)
        print(
            "    {} bin {}  RGB{} -> L={:7.3f}  a={:8.3f}  b={:8.3f}".format(
                nombre, i + 1, color, L, a, b
            )
        )

#  i.  matriz de costos
print("\nSemana 03 - b) i.  matriz de costos (distancia euclidiana en CIE LAB):")
costos = costMatrix(COLORES_1, COLORES_2)
print(Matrix(costos).display(decimal_places=2))

#  ii.  una matriz de flujos valida
print("\nSemana 03 - b) ii.  matriz de flujos (celdas mas baratas primero):")
flujos = greedyByCostFlow(PESOS_1, PESOS_2, costos)
print(Matrix(flujos).display(decimal_places=2))
print(
    "  sumas por fila: {}  (deben ser {})".format(
        np.round(flujos.sum(axis=1), 4).tolist(), PESOS_1
    )
)
print(
    "  sumas por col : {}  (deben ser {})".format(
        np.round(flujos.sum(axis=0), 4).tolist(), PESOS_2
    )
)
print("  flujo valido:", isValidFlow(flujos, PESOS_1, PESOS_2))

#  iii.  EMD
print("\nSemana 03 - b) iii.  EMD:")
print("  trabajo total = {:.4f}".format((costos * flujos).sum()))
print("  flujo total   = {:.4f}".format(flujos.sum()))
print("  EMD           = {:.4f}".format(emd(costos, flujos)))

# =====================================================================
# SEMANA 04 - audio PCM
# =====================================================================
DURACION = 60 + 37  # 1 minuto 37 segundos
CANALES = 1

print("\n" + "=" * 60)
print("SEMANA 04 - audio PCM ({} s, {} canal)".format(DURACION, CANALES))

print("\nSemana 04 - i.  A.raw (s16le, 44100 Hz):")
_, techo_a = describePCM("A.raw", DURACION, 44100, 16, CANALES)

print("\nSemana 04 - ii.  B.raw (32f, 8192 Hz):")
_, techo_b = describePCM("B.raw", DURACION, 8192, 32, CANALES)

print("\nSemana 04 - iii.  C.raw (s16le, 44100 Hz, convertido desde B.raw):")
# remuestrear hacia arriba no recupera lo que B.raw ya perdio
describePCM("C.raw", DURACION, 44100, 16, CANALES, contentLimitHz=techo_b)
