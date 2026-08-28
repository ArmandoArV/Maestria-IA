import t1_util


class Coincidencia:
    def __init__(self, imagen_q, imagen_r, distancia):
        self._imagen_q = str(imagen_q)
        self._imagen_r = str(imagen_r)
        self._distancia = float(distancia)

    @property
    def imagen_q(self):
        return self._imagen_q

    @property
    def imagen_r(self):
        return self._imagen_r

    @property
    def distancia(self):
        return self._distancia

    def columnas(self, decimales=4):
        return [self._imagen_q, self._imagen_r,
                "{:.{}f}".format(self._distancia, decimales)]

    def __repr__(self):
        return "\t".join(self.columnas())


class ResultsWriter:
    def __init__(self, decimales=4):
        self.decimales = decimales

    @property
    def decimales(self):
        return self._decimales

    @decimales.setter
    def decimales(self, valor):
        valor = int(valor)
        if valor < 0:
            raise ValueError("decimales debe ser >= 0, recibí {}".format(valor))
        self._decimales = valor

    def escribir(self, archivo_salida, coincidencias):
        t1_util.escribir_lista_de_columnas_en_archivo(
            [c.columnas(self._decimales) for c in coincidencias], archivo_salida)

    def __repr__(self):
        return "ResultsWriter(decimales={})".format(self.decimales)
