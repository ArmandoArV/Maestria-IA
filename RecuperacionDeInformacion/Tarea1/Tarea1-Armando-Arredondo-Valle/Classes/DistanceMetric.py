import abc

import scipy.spatial


class DistanceMetric(abc.ABC):
    @property
    @abc.abstractmethod
    def nombre(self):
        pass

    def matriz(self, A, B):
        return scipy.spatial.distance.cdist(A, B, metric=self.nombre)

    @staticmethod
    def crear(metrica):
        if isinstance(metrica, DistanceMetric):
            return metrica
        conocidas = {"cityblock": L1Distance, "l1": L1Distance, "manhattan": L1Distance,
                     "euclidean": L2Distance, "l2": L2Distance,
                     "chebyshev": LInfDistance, "linf": LInfDistance}
        clave = str(metrica).lower()
        if clave not in conocidas:
            raise ValueError("no conozco la métrica {}, use una de {}".format(
                metrica, sorted(conocidas)))
        return conocidas[clave]()

    def __repr__(self):
        return "{}('{}')".format(type(self).__name__, self.nombre)


class L1Distance(DistanceMetric):
    @property
    def nombre(self):
        return "cityblock"


class L2Distance(DistanceMetric):
    @property
    def nombre(self):
        return "euclidean"


class LInfDistance(DistanceMetric):
    @property
    def nombre(self):
        return "chebyshev"
