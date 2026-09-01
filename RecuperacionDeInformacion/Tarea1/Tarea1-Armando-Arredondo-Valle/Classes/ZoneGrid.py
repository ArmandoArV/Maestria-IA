class Zona:
    def __init__(self, nivel, fila, col, rect, histograma=None):
        self._nivel = int(nivel)
        self._fila = int(fila)
        self._col = int(col)
        self._rect = tuple(rect)
        self.histograma = histograma

    @property
    def nivel(self):
        return self._nivel

    @property
    def fila(self):
        return self._fila

    @property
    def col(self):
        return self._col

    @property
    def rect(self):
        return self._rect

    @property
    def ancho(self):
        return self._rect[2] - self._rect[0]

    @property
    def alto(self):
        return self._rect[3] - self._rect[1]

    @property
    def histograma(self):
        return self._histograma

    @histograma.setter
    def histograma(self, valor):
        self._histograma = valor

    def recortar(self, imagen):
        x0, y0, x1, y1 = self._rect
        return imagen[y0:y1, x0:x1]

    def __repr__(self):
        return "Zona(nivel={}, fila={}, col={}, rect={})".format(
            self.nivel, self.fila, self.col, self.rect)


class ZoneGrid:
    def __init__(self, niveles):
        self.niveles = niveles

    @property
    def niveles(self):
        return list(self._niveles)

    @niveles.setter
    def niveles(self, valor):
        niveles = [int(n) for n in valor]
        if not niveles or any(n < 1 for n in niveles):
            raise ValueError("niveles debe ser una lista de enteros >= 1, recibí {}".format(valor))
        self._niveles = niveles

    @property
    def cantidad_zonas(self):
        return sum(nivel * nivel for nivel in self._niveles)

    @staticmethod
    def limites(maximo_no_incluido, cantidad):
        lista = [round(maximo_no_incluido * i / cantidad) for i in range(cantidad)]
        lista.append(maximo_no_incluido)
        return lista

    def zonas(self, alto, ancho):
        for nivel in self._niveles:
            ly = self.limites(alto, nivel)
            lx = self.limites(ancho, nivel)
            for fila in range(nivel):
                for col in range(nivel):
                    rect = (lx[col], ly[fila], lx[col + 1], ly[fila + 1])
                    yield Zona(nivel, fila, col, rect)

    def zonas_de(self, imagen):
        for zona in self.zonas(imagen.shape[0], imagen.shape[1]):
            yield zona, zona.recortar(imagen)

    @classmethod
    def desde_config(cls, config):
        return cls(config.niveles)

    def __repr__(self):
        return "ZoneGrid(niveles={}, {} zonas)".format(self.niveles, self.cantidad_zonas)
