"""Tamano y frecuencia maxima de archivos PCM sin comprimir (Semana 04)."""


def pcmSize(seconds, sampleRate, bitsPerSample, channels=1):
    """Tamano exacto en bytes de un PCM crudo (sin cabecera)."""
    return int(seconds * sampleRate * (bitsPerSample // 8) * channels)


def nyquist(sampleRate):
    """Frecuencia maxima representable segun Nyquist."""
    return sampleRate / 2


def describePCM(nombre, seconds, sampleRate, bitsPerSample, channels=1,
                contentLimitHz=None):
    """Imprime tamano, Nyquist y el techo real del contenido."""
    tam = pcmSize(seconds, sampleRate, bitsPerSample, channels)
    nyq = nyquist(sampleRate)
    techo = nyq if contentLimitHz is None else min(nyq, contentLimitHz)
    print("  {}: {} bytes  ({} s x {} Hz x {} bits x {} canal)".format(
        nombre, tam, seconds, sampleRate, bitsPerSample, channels))
    print("     Nyquist del formato : {:.0f} Hz".format(nyq))
    print("     frecuencia maxima   : {:.0f} Hz".format(techo))
    return tam, techo
