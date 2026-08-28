import cv2


class ColorHistogram3D:
    CANALES = [0, 1, 2]
    RANGO = [0, 256, 0, 256, 0, 256]

    def __init__(self, bins=8):
        self.bins = bins

    @property
    def bins(self):
        return self._bins

    @bins.setter
    def bins(self, valor):
        valor = int(valor)
        if not 1 <= valor <= 256:
            raise ValueError("bins debe estar entre 1 y 256, recibí {}".format(valor))
        self._bins = valor

    @property
    def largo(self):
        return self._bins ** 3

    def contar(self, region_bgr):
        bins = self._bins
        return cv2.calcHist([region_bgr], self.CANALES, None,
                            [bins, bins, bins], self.RANGO).flatten()

    @staticmethod
    def normalizar(histograma):
        suma = histograma.sum()
        if suma > 0:
            histograma = histograma / suma
        return histograma

    def calcular(self, region_bgr):
        return self.normalizar(self.contar(region_bgr))

    @classmethod
    def desde_config(cls, config):
        return cls(bins=config.bins)

    def __repr__(self):
        return "ColorHistogram3D(bins={}, largo={})".format(self.bins, self.largo)
