import numpy as np

from Functions.kernels import SOBEL_X, SOBEL_Y
from Functions.validateConvolution import validateConvolution


def gradient(image, kernel_x=SOBEL_X, kernel_y=SOBEL_Y):
    """Devuelve (Ix, Iy) como numpy arrays, sólo en la zona válida.

    Usa correlación (reflect_kernel=False), que es lo que hace cv2.Sobel() y
    lo que usa el código del curso. Con convolución (kernel volteado) el signo
    de Ix e Iy se invierte y el ángulo del gradiente sale girado en 180°.
    """
    ix = np.asarray(validateConvolution(np.asarray(image, dtype=np.float32), kernel_x,
                                        reflect_kernel=False))
    iy = np.asarray(validateConvolution(np.asarray(image, dtype=np.float32), kernel_y,
                                        reflect_kernel=False))
    return ix, iy


def gradientMagnitude(ix, iy):
    return np.sqrt(np.square(ix) + np.square(iy))


def gradientAngle(ix, iy, range180=True):
    """Ángulo del gradiente en grados.

    range180=True  -> [-180, 180]  (distingue el sentido del borde)
    range180=False -> (-90, 90]    (sólo la dirección del borde)

    Devuelve NaN donde la magnitud es 0 (el ángulo no está definido).
    """
    angulos = np.degrees(np.arctan2(iy, ix))
    angulos = np.where(gradientMagnitude(ix, iy) == 0, np.nan, angulos)
    if not range180:
        angulos = np.where(angulos <= -90, angulos + 180, angulos)
        angulos = np.where(angulos > 90, angulos - 180, angulos)
    return angulos
