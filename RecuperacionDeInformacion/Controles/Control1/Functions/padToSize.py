import numpy as np

from Classes.Matrix import Matrix


def padToSize(valid, shape, filler=""):
    valid = np.asarray(valid)
    alto, ancho = shape
    margen_y = (alto - valid.shape[0]) // 2
    margen_x = (ancho - valid.shape[1]) // 2
    data = [[filler for _ in range(ancho)] for _ in range(alto)]
    for y in range(valid.shape[0]):
        for x in range(valid.shape[1]):
            valor = valid[y, x]
            data[y + margen_y][x + margen_x] = filler if valor is None or (
                isinstance(valor, float) and np.isnan(valor)) else valor
    return Matrix(data)
