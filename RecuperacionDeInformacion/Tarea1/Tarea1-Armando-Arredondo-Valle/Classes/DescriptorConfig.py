import json
import os


class DescriptorConfig:
    ARCHIVO = "config.json"

    def __init__(self, size=128, grid=4, usar_global=True, bins=8, equalizar=True):
        self.size = size
        self.grid = grid
        self.usar_global = usar_global
        self.bins = bins
        self.equalizar = equalizar

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
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, valor):
        valor = int(valor)
        if valor < 1:
            raise ValueError("grid debe ser >= 1, recibí {}".format(valor))
        self._grid = valor

    @property
    def usar_global(self):
        return self._usar_global

    @usar_global.setter
    def usar_global(self, valor):
        self._usar_global = bool(valor)

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
    def equalizar(self):
        return self._equalizar

    @equalizar.setter
    def equalizar(self, valor):
        self._equalizar = bool(valor)

    @property
    def niveles(self):
        return ([1] if self.usar_global else []) + [self.grid]

    @property
    def cantidad_zonas(self):
        return sum(nivel * nivel for nivel in self.niveles)

    @property
    def largo_descriptor(self):
        return self.cantidad_zonas * (self.bins ** 3)

    def to_dict(self):
        return {"size": self.size, "grid": self.grid, "usar_global": self.usar_global,
                "bins": self.bins, "equalizar": self.equalizar}

    @classmethod
    def from_dict(cls, datos):
        return cls(**datos)

    def guardar(self, carpeta):
        os.makedirs(carpeta, exist_ok=True)
        with open(os.path.join(carpeta, self.ARCHIVO), "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def cargar(cls, carpeta):
        ruta = os.path.join(carpeta, cls.ARCHIVO)
        if not os.path.isfile(ruta):
            return cls()
        with open(ruta, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))

    def __eq__(self, otra):
        return isinstance(otra, DescriptorConfig) and self.to_dict() == otra.to_dict()

    def __repr__(self):
        return "DescriptorConfig({}) -> {} zonas, {} dimensiones".format(
            self.to_dict(), self.cantidad_zonas, self.largo_descriptor)
