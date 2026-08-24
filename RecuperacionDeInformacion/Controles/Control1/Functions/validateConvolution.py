import cv2
import numpy as np

from Classes.Matrix import Matrix


def _as_array(m):
    """Acepta indistintamente un Matrix, una lista de listas o un numpy array."""
    if isinstance(m, Matrix):
        return m.to_array(np.float32)
    return np.asarray(m)


def validateConvolution(image, kernel, reflect_kernel=False):
    returnMatrix = isinstance(image, Matrix)
    image = _as_array(image)
    kernel = _as_array(kernel)
    if reflect_kernel:
        kernel = cv2.flip(kernel, -1)  # Reflect the kernel if specified
    # Get the dimensions of the image and kernel
    height_k, width_k = kernel.shape
    output = np.zeros((image.shape[0] - height_k + 1, image.shape[1] - width_k + 1))
    for y in range(output.shape[0]):
        for x in range(output.shape[1]):
            # Extract the region of interest from the image
            region = image[y:y + height_k, x:x + width_k]
            # Perform element-wise multiplication and sum the result
            output[y, x] = np.sum(region * kernel)
    # si entró un Matrix, sale un Matrix (para poder imprimirlo con display())
    return Matrix(output) if returnMatrix else output
