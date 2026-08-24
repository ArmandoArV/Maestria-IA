import matplotlib.pyplot as plt
import numpy as np

from Functions.histogram import binLimits
from Functions.hog import angleBinLimits

# paleta: una sola serie -> un solo color, sin leyenda (el título nombra la serie)
SURFACE = "#fcfcfb"
SERIES = "#2a78d6"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e3e2df"

# a partir de esta cantidad de barras no se etiqueta cada altura (quedaría ilegible)
MAX_ETIQUETAS = 16


def _estilo(ax):
    """Ejes recesivos: sin marco arriba/derecha y grilla horizontal tenue por detrás."""
    ax.set_facecolor(SURFACE)
    ax.figure.set_facecolor(SURFACE)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(GRID)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(colors=TEXT_SECONDARY, labelsize=8, length=0)


def _etiquetar(ax, alturas, decimales=4):
    """Escribe la altura sobre las barras distintas de cero (sólo si son pocas)."""
    no_cero = [i for i, v in enumerate(alturas) if v > 0]
    if len(no_cero) > MAX_ETIQUETAS:
        return
    ultimo = len(alturas) - 1
    for i in no_cero:
        # las barras de los extremos se etiquetan hacia adentro para no chocar con los ejes
        if i == 0:
            alineacion, desplazamiento = "left", (2, 5)
        elif i == ultimo:
            alineacion, desplazamiento = "right", (-2, 5)
        else:
            alineacion, desplazamiento = "center", (0, 5)
        ax.annotate(_formato(alturas[i], decimales), (i, alturas[i]),
                    textcoords="offset points", xytext=desplazamiento,
                    ha=alineacion, fontsize=8, color=TEXT_PRIMARY)


def _formato(valor, decimales=4):
    """Altura con hasta `decimales` decimales, sin ceros de relleno pero mínimo 2."""
    texto = "{:.{}f}".format(valor, decimales).rstrip("0")
    entero, _, decimal = texto.partition(".")
    return "{}.{}".format(entero, decimal.ljust(2, "0"))


def _dibujar_histograma(ax, histograma, etiquetas_x, titulo, xlabel, decimales=4):
    histograma = np.asarray(histograma, dtype=float)
    n = len(histograma)
    # barras contiguas cuando son muchas (histograma de grises), con separación si son pocas
    ancho = 1.0 if n > 32 else 0.85
    ax.bar(range(n), histograma, width=ancho, color=SERIES, edgecolor="none")
    _estilo(ax)
    _etiquetar(ax, histograma, decimales)
    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(0, max(1e-9, histograma.max()) * 1.28)
    if etiquetas_x is not None:
        posiciones, textos = etiquetas_x
        ax.set_xticks(posiciones)
        ax.set_xticklabels(textos)
    ax.set_xlabel(xlabel, fontsize=8, color=TEXT_SECONDARY)
    ax.set_ylabel("frecuencia normalizada", fontsize=8, color=TEXT_SECONDARY)
    ax.set_title(titulo, fontsize=10, color=TEXT_PRIMARY, loc="left", pad=10)


def _ticks_grises(bins, maxValue):
    """Ticks del eje x de un histograma de grises: el tono en que empieza cada bin."""
    limites = binLimits(bins, maxValue)
    paso = max(1, bins // 8)
    posiciones = list(range(0, bins, paso))
    return posiciones, [str(limites[p]) for p in posiciones]


def _ticks_angulos(bins, range180):
    """Ticks del eje x de un HOG: el rango de ángulos que cubre cada bin."""
    limites = angleBinLimits(bins, range180)
    return (range(bins),
            ["({:g}, {:g}]".format(limites[b], limites[b + 1]) for b in range(bins)])


def _cerrar(fig, savePath):
    fig.tight_layout()
    if savePath:
        fig.savefig(savePath, dpi=200, facecolor=SURFACE)
        plt.close(fig)
        print("   gráfico guardado en {}".format(savePath))
    else:
        plt.show()


def plotHistogram(histogram, title="Histograma de intensidades", maxValue=256,
                  savePath=None):
    """Histograma de grises de una imagen completa."""
    histogram = np.asarray(histogram, dtype=float)
    fig, ax = plt.subplots(figsize=(9, 3.4))
    _dibujar_histograma(ax, histogram, _ticks_grises(len(histogram), maxValue),
                        "{} ({} bins)".format(title, len(histogram)),
                        "tono de gris en que comienza el bin")
    _cerrar(fig, savePath)


def plotHistogramsByZones(zones, title="Histograma por zonas", maxValue=256,
                          zonesX=2, zonesY=2, savePath=None):
    """Un gráfico por zona (small multiples), todos con la misma escala en y.

    `zones` es lo que devuelve histogramByZones(): lista de (fila, columna, histograma).
    """
    maximo = max(np.asarray(h).max() for _, _, h in zones)
    fig, axes = plt.subplots(zonesY, zonesX, figsize=(5.2 * zonesX, 3.0 * zonesY),
                             squeeze=False)
    for fila, columna, histograma in zones:
        ax = axes[fila][columna]
        _dibujar_histograma(ax, histograma,
                            _ticks_grises(len(histograma), maxValue),
                            "zona fila {} · columna {} ({} bins)".format(
                                fila + 1, columna + 1, len(histograma)),
                            "tono de gris en que comienza el bin")
        ax.set_ylim(0, max(1e-9, maximo) * 1.28)
    fig.suptitle(title, fontsize=11, color=TEXT_PRIMARY, x=0.01, ha="left")
    _cerrar(fig, savePath)


def plotAngleHistogram(histogram, title="HOG", range180=False, savePath=None):
    """Histograma de orientaciones del gradiente."""
    histogram = np.asarray(histogram, dtype=float)
    fig, ax = plt.subplots(figsize=(7.5, 3.4))
    _dibujar_histograma(ax, histogram, _ticks_angulos(len(histogram), range180),
                        "{} ({} bins)".format(title, len(histogram)),
                        "rango de ángulos del bin (grados)")
    ax.tick_params(axis="x", labelrotation=45)
    _cerrar(fig, savePath)


def plotHOGByZones(zones, title="HOG por zonas", range180=False, zonesX=2, zonesY=2,
                   savePath=None):
    """Un HOG por zona (small multiples). `zones` es lo que devuelve hog()."""
    maximo = max(np.asarray(h).max() for _, _, h in zones)
    fig, axes = plt.subplots(zonesY, zonesX, figsize=(5.4 * zonesX, 3.4 * zonesY),
                             squeeze=False)
    for fila, columna, histograma in zones:
        ax = axes[fila][columna]
        _dibujar_histograma(ax, histograma, _ticks_angulos(len(histograma), range180),
                            "zona fila {} · columna {} ({} bins)".format(
                                fila + 1, columna + 1, len(histograma)),
                            "rango de ángulos del bin (grados)")
        ax.tick_params(axis="x", labelrotation=45)
        ax.set_ylim(0, max(1e-9, maximo) * 1.28)
    fig.suptitle(title, fontsize=11, color=TEXT_PRIMARY, x=0.01, ha="left")
    _cerrar(fig, savePath)
