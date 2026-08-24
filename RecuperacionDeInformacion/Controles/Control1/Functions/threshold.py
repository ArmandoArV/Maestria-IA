import numpy as np

from Classes.Matrix import Matrix


def threshold(image, t, high=255, low=0, useAbs=True):
    devolver_matrix = isinstance(image, Matrix)
    imagen = np.asarray(image, dtype=np.float32)
    valores = np.abs(imagen) if useAbs else imagen
    output = np.where(valores >= t, float(high), float(low))
    return Matrix(output) if devolver_matrix else output
