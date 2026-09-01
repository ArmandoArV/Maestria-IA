import os

import numpy

from Classes.DescriptorConfig import DescriptorConfig


class DescriptorIndex:
    ARCHIVO = "descriptores.npz"

    def __init__(self, nombres, matriz, config):
        nombres = list(nombres)
        if len(nombres) != matriz.shape[0]:
            raise ValueError("nombres y matriz no calzan: {} vs {}".format(
                len(nombres), matriz.shape[0]))
        self._nombres = nombres
        self._matriz = matriz
        self._config = config

    @property
    def nombres(self):
        return self._nombres

    @property
    def matriz(self):
        return self._matriz

    @property
    def config(self):
        return self._config

    @property
    def dimensiones(self):
        return self._matriz.shape[1]

    def nombre_de(self, fila):
        return self._nombres[int(fila)]

    def descriptor_de(self, nombre):
        return self._matriz[self._nombres.index(nombre)]

    def __len__(self):
        return len(self._nombres)

    @classmethod
    def construir(cls, dataset, descriptor, flip=False, verbose=False, cada=200):
        matriz = numpy.zeros((len(dataset), descriptor.largo), numpy.float32)
        for k, (nombre, imagen) in enumerate(dataset):
            matriz[k] = descriptor.describir(imagen, flip=flip)
            cls._avisar(verbose, cada, k, len(dataset))
        return cls(dataset.nombres, matriz, descriptor.config)

    @classmethod
    def construir_con_reflejo(cls, dataset, descriptor, verbose=False, cada=200):
        normal = numpy.zeros((len(dataset), descriptor.largo), numpy.float32)
        reflejo = numpy.zeros((len(dataset), descriptor.largo), numpy.float32)
        for k, (nombre, imagen) in enumerate(dataset):
            normal[k] = descriptor.describir(imagen, flip=False)
            reflejo[k] = descriptor.describir(imagen, flip=True)
            cls._avisar(verbose, cada, k, len(dataset))
        return (cls(dataset.nombres, normal, descriptor.config),
                cls(dataset.nombres, reflejo, descriptor.config))

    @staticmethod
    def _avisar(verbose, cada, k, total):
        if verbose and (k + 1) % cada == 0:
            print("  procesadas {}/{} imágenes...".format(k + 1, total))

    def guardar(self, carpeta):
        os.makedirs(carpeta, exist_ok=True)
        numpy.savez_compressed(os.path.join(carpeta, self.ARCHIVO),
                               nombres=numpy.array(self._nombres),
                               descriptores=self._matriz)
        self._config.guardar(carpeta)

    @classmethod
    def cargar(cls, carpeta):
        ruta = os.path.join(carpeta, cls.ARCHIVO)
        if not os.path.isfile(ruta):
            raise FileNotFoundError(
                "no existe {} (¿terminó bien tarea1-parte1.py?)".format(ruta))
        datos = numpy.load(ruta, allow_pickle=True)
        nombres = [str(n) for n in datos["nombres"]]
        matriz = datos["descriptores"].astype(numpy.float32)
        return cls(nombres, matriz, DescriptorConfig.cargar(carpeta))

    def __repr__(self):
        return "DescriptorIndex({} imágenes x {} dimensiones)".format(
            len(self), self.dimensiones)
