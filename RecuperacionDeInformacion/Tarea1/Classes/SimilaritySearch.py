import numpy

from Classes.DistanceMetric import DistanceMetric, L1Distance
from Classes.SearchResult import Coincidencia


class SimilaritySearch:
    def __init__(self, indice_R, metrica=None, bloque=500):
        self._indice_R = indice_R
        self.metrica = metrica if metrica is not None else L1Distance()
        self.bloque = bloque

    @property
    def indice_R(self):
        return self._indice_R

    @property
    def metrica(self):
        return self._metrica

    @metrica.setter
    def metrica(self, valor):
        self._metrica = DistanceMetric.crear(valor)

    @property
    def bloque(self):
        return self._bloque

    @bloque.setter
    def bloque(self, valor):
        valor = int(valor)
        if valor < 1:
            raise ValueError("bloque debe ser >= 1, recibí {}".format(valor))
        self._bloque = valor

    def distancias(self, matriz_Q):
        return self._metrica.matriz(matriz_Q, self._indice_R.matriz)

    def _distancias_del_bloque(self, indice_Q, indice_Q_reflejado, inicio, fin):
        D = self.distancias(indice_Q.matriz[inicio:fin])
        if indice_Q_reflejado is not None:
            numpy.minimum(D, self.distancias(indice_Q_reflejado.matriz[inicio:fin]), out=D)
        return D

    @staticmethod
    def _mas_cercanos(D):
        columnas = numpy.argmin(D, axis=1)
        return columnas, D[numpy.arange(D.shape[0]), columnas]

    def buscar(self, indice_Q, indice_Q_reflejado=None):
        resultados = []
        for inicio in range(0, len(indice_Q), self._bloque):
            fin = min(inicio + self._bloque, len(indice_Q))
            D = self._distancias_del_bloque(indice_Q, indice_Q_reflejado, inicio, fin)
            columnas, distancias = self._mas_cercanos(D)
            for k in range(fin - inicio):
                resultados.append(Coincidencia(indice_Q.nombre_de(inicio + k),
                                               self._indice_R.nombre_de(columnas[k]),
                                               distancias[k]))
        return resultados

    def __repr__(self):
        return "SimilaritySearch(R={}, metrica={}, bloque={})".format(
            len(self._indice_R), self._metrica.nombre, self._bloque)
