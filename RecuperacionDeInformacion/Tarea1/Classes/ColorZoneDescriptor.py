import numpy

from Classes.ColorHistogram3D import ColorHistogram3D
from Classes.Descriptor import Descriptor
from Classes.DescriptorConfig import DescriptorConfig
from Classes.ImagePreprocessor import ImagePreprocessor
from Classes.ZoneGrid import ZoneGrid


class ColorZoneDescriptor(Descriptor):
    def __init__(self, config=None):
        self.config = config if config is not None else DescriptorConfig()

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, valor):
        if not isinstance(valor, DescriptorConfig):
            raise TypeError(
                "config debe ser un DescriptorConfig, recibí {}".format(type(valor))
            )
        self._config = valor
        self._preprocesador = ImagePreprocessor.desde_config(valor)
        self._grilla = ZoneGrid.desde_config(valor)
        self._histograma = ColorHistogram3D.desde_config(valor)

    @property
    def preprocesador(self):
        return self._preprocesador

    @property
    def grilla(self):
        return self._grilla

    @property
    def histograma(self):
        return self._histograma

    @property
    def largo(self):
        return self._grilla.cantidad_zonas * self._histograma.largo

    def describir(self, imagen_bgr, flip=False):
        return self._concatenar(self._describir_zonas(imagen_bgr, flip))

    def describir_con_zonas(self, imagen_bgr, flip=False):
        preparada = self.preparar(imagen_bgr, flip)
        zonas = list(self._describir_zonas(preparada, flip=False, ya_preparada=True))
        return self._concatenar(zonas), zonas, preparada

    def preparar(self, imagen_bgr, flip=False):
        if flip:
            imagen_bgr = self._preprocesador.reflejar(imagen_bgr)
        return self._preprocesador.preparar(imagen_bgr)

    def _describir_zonas(self, imagen_bgr, flip=False, ya_preparada=False):
        imagen = imagen_bgr if ya_preparada else self.preparar(imagen_bgr, flip)
        for zona, region in self._grilla.zonas_de(imagen):
            zona.histograma = self._histograma.calcular(region)
            yield zona

    @staticmethod
    def _concatenar(zonas):
        return numpy.concatenate([zona.histograma for zona in zonas]).astype(
            numpy.float32
        )
