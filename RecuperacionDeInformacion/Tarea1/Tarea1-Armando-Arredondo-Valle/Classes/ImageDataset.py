import os

import cv2

import t1_util


class ImageDataset:
    def __init__(self, carpeta, extension=".jpg"):
        self._extension = str(extension)
        self.carpeta = carpeta

    @property
    def carpeta(self):
        return self._carpeta

    @carpeta.setter
    def carpeta(self, valor):
        if not os.path.isdir(valor):
            raise NotADirectoryError("no existe directorio {}".format(valor))
        self._carpeta = valor
        self._nombres = self._listar()

    @property
    def extension(self):
        return self._extension

    @extension.setter
    def extension(self, valor):
        self._extension = str(valor)
        self._nombres = self._listar()

    @property
    def nombres(self):
        return self._nombres

    def _listar(self):
        nombres = t1_util.listar_archivos_con_extension(self._carpeta, self._extension)
        if not nombres:
            raise FileNotFoundError("no hay imágenes {} en {}".format(
                self._extension, self._carpeta))
        return nombres

    def ruta(self, nombre):
        return os.path.join(self._carpeta, nombre)

    def leer(self, nombre):
        imagen = cv2.imread(self.ruta(nombre), cv2.IMREAD_COLOR)
        if imagen is None:
            raise IOError("no puedo abrir la imagen: " + self.ruta(nombre))
        return imagen

    def __len__(self):
        return len(self._nombres)

    def __iter__(self):
        for nombre in self._nombres:
            yield nombre, self.leer(nombre)

    def __repr__(self):
        return "ImageDataset({}, {} imágenes)".format(self._carpeta, len(self))
