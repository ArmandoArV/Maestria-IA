import cv2


class ImagePreprocessor:
    def __init__(self, size=128, equalizar=True, interpolacion=cv2.INTER_AREA):
        self.size = size
        self.equalizar = equalizar
        self.interpolacion = interpolacion

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, valor):
        valor = int(valor)
        if valor < 1:
            raise ValueError("size debe ser >= 1, recibí {}".format(valor))
        self._size = valor

    @property
    def equalizar(self):
        return self._equalizar

    @equalizar.setter
    def equalizar(self, valor):
        self._equalizar = bool(valor)

    @property
    def interpolacion(self):
        return self._interpolacion

    @interpolacion.setter
    def interpolacion(self, valor):
        self._interpolacion = int(valor)

    def redimensionar(self, imagen_bgr):
        return cv2.resize(imagen_bgr, (self.size, self.size),
                          interpolation=self.interpolacion)

    @staticmethod
    def ecualizar_canales(imagen_bgr):
        return cv2.merge([cv2.equalizeHist(canal) for canal in cv2.split(imagen_bgr)])

    @staticmethod
    def reflejar(imagen_bgr):
        return cv2.flip(imagen_bgr, 1)

    def preparar(self, imagen_bgr):
        imagen = self.redimensionar(imagen_bgr)
        if self.equalizar:
            imagen = self.ecualizar_canales(imagen)
        return imagen

    @classmethod
    def desde_config(cls, config):
        return cls(size=config.size, equalizar=config.equalizar)

    def __repr__(self):
        return "ImagePreprocessor(size={}, equalizar={})".format(self.size, self.equalizar)
