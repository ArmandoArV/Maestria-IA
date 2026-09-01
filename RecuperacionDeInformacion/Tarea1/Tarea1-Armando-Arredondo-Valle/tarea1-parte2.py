import sys
import os
import time

from Classes import (ColorZoneDescriptor, DescriptorIndex, ImageDataset, L1Distance,
                     ResultsWriter, SimilaritySearch)

TOLERAR_REFLEJO = True
METRICA = L1Distance()


def tarea1_parte2(dir_input_imagenes_Q, dir_input_descriptores_R, file_output_resultados):
    if not os.path.isdir(dir_input_imagenes_Q):
        print("ERROR: no existe directorio {}".format(dir_input_imagenes_Q))
        sys.exit(1)
    elif not os.path.isdir(dir_input_descriptores_R):
        print("ERROR: no existe directorio {} (¿terminó bien tarea1-parte1.py?)".format(dir_input_descriptores_R))
        sys.exit(1)
    elif os.path.exists(file_output_resultados):
        print("ERROR: ya existe archivo {}".format(file_output_resultados))
        sys.exit(1)

    indice_R = DescriptorIndex.cargar(dir_input_descriptores_R)
    print("[parte2] R: {}".format(indice_R))

    imagenes_Q = ImageDataset(dir_input_imagenes_Q)
    descriptor = ColorZoneDescriptor(indice_R.config)
    print("[parte2] {} imágenes en {}".format(len(imagenes_Q), dir_input_imagenes_Q))
    t0 = time.time()
    if TOLERAR_REFLEJO:
        indice_Q, indice_Q_reflejado = DescriptorIndex.construir_con_reflejo(
            imagenes_Q, descriptor, verbose=True)
    else:
        indice_Q = DescriptorIndex.construir(imagenes_Q, descriptor, verbose=True)
        indice_Q_reflejado = None
    print("[parte2] Q: {} en {:.1f} s".format(indice_Q, time.time() - t0))

    t0 = time.time()
    busqueda = SimilaritySearch(indice_R, metrica=METRICA)
    resultados = busqueda.buscar(indice_Q, indice_Q_reflejado)
    print("[parte2] búsqueda terminada en {:.1f} s".format(time.time() - t0))

    ResultsWriter().escribir(file_output_resultados, resultados)
    print("[parte2] resultados escritos en: {}".format(file_output_resultados))


if len(sys.argv) < 4:
    print("Uso: {}  dir_input_imagenes_Q  dir_input_descriptores_R  file_output_resultados".format(sys.argv[0]))
    sys.exit(1)

dir_input_imagenes_Q = sys.argv[1]
dir_input_descriptores_R = sys.argv[2]
file_output_resultados = sys.argv[3]

tarea1_parte2(dir_input_imagenes_Q, dir_input_descriptores_R, file_output_resultados)
