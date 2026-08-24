import numpy as np

from Classes.Matrix import Matrix


def medianFilter(image, n=3):
    devolver_matrix = isinstance(image, Matrix)
    imagen = np.asarray(image, dtype=np.float32)
    if n % 2 == 0:
        raise ValueError("el tamaño de la ventana debe ser impar")
    output = np.zeros((imagen.shape[0] - n + 1, imagen.shape[1] - n + 1))
    for y in range(output.shape[0]):
        for x in range(output.shape[1]):
            ventana = imagen[y:y + n, x:x + n]
            # la mediana es el valor central al ordenar los n*n valores
            output[y, x] = np.median(ventana)
    return Matrix(output) if devolver_matrix else output
