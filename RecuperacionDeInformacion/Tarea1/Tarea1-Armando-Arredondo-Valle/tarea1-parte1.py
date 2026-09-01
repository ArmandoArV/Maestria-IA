import sys
import os
import time

from Classes import ColorZoneDescriptor, DescriptorConfig, DescriptorIndex, ImageDataset

CONFIG = DescriptorConfig(size=128, grid=4, usar_global=True, bins=8, equalizar=True)


def tarea1_parte1(dir_input_imagenes_R, dir_output_descriptores_R):
    if not os.path.isdir(dir_input_imagenes_R):
        print("ERROR: no existe directorio {}".format(dir_input_imagenes_R))
        sys.exit(1)
    elif os.path.exists(dir_output_descriptores_R):
        print("ERROR: ya existe directorio {}".format(dir_output_descriptores_R))
        sys.exit(1)

    imagenes_R = ImageDataset(dir_input_imagenes_R)
    print("[parte1] {} imágenes en {}".format(len(imagenes_R), dir_input_imagenes_R))

    descriptor = ColorZoneDescriptor(CONFIG)
    print("[parte1] descriptor: {}".format(descriptor))
    t0 = time.time()
    indice_R = DescriptorIndex.construir(imagenes_R, descriptor, verbose=True)
    print("[parte1] {} en {:.1f} s".format(indice_R, time.time() - t0))

    indice_R.guardar(dir_output_descriptores_R)
    print("[parte1] descriptores guardados en: {}".format(dir_output_descriptores_R))


if len(sys.argv) < 3:
    print("Uso: {}  dir_input_imagenes_R  dir_output_descriptores_R".format(sys.argv[0]))
    sys.exit(1)

dir_input_imagenes_R = sys.argv[1]
dir_output_descriptores_R = sys.argv[2]

tarea1_parte1(dir_input_imagenes_R, dir_output_descriptores_R)
