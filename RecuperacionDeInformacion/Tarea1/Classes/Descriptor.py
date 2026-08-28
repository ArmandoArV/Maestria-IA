import abc


class Descriptor(abc.ABC):
    @property
    @abc.abstractmethod
    def largo(self):
        pass

    @property
    @abc.abstractmethod
    def config(self):
        pass

    @abc.abstractmethod
    def describir(self, imagen_bgr, flip=False):
        pass

    def __repr__(self):
        return "{}({} dimensiones)".format(type(self).__name__, self.largo)
