"""
Generazione di gratings di calibrazione per SLM Santec con livelli di grigio 10-bit (0-1023).
"""

import os
import numpy as np
from PIL import Image
from tqdm import tqdm


def graylevel_to_rgb10bit(graylevel):
    """
    Converte un valore di grigio a 10-bit (0-1023) in un formato BMP RGB 8-bit compatibile con Santec.

    Args:
        graylevel (numpy.ndarray): Array 2D di valori interi da 0 a 1023.

    Returns:
        numpy.ndarray: Immagine RGB a 8-bit con codifica 10-bit.
    """
    graylevel = np.clip(graylevel, 0, 1023).astype(np.uint16)

    # Calcola i canali RGB secondo la tabella del manuale Santec
    r = ((graylevel >> 7) & 0x07) * 32  # 3 bit (shift 7, maschera 0x07)
    g = ((graylevel >> 4) & 0x07) * 32  # 3 bit (shift 4, maschera 0x07)
    b = (graylevel & 0x0F) * 16         # 4 bit (maschera 0x0F)

    # Combina i canali e converti in uint8
    return np.stack((r, g, b), axis=2).astype(np.uint8)


def create_striped_bmp_10bit(width, height, period, value1, value2, foldername, filename):
    """
    Crea un'immagine BMP a bande alternate con livelli di grigio a 10-bit.

    Args:
        width (int): Larghezza dell'immagine.
        height (int): Altezza dell'immagine.
        period (int): Periodo delle bande in pixel.
        value1 (int): Livello di grigio per le bande pari (0-1023).
        value2 (int): Livello di grigio per le bande dispari (0-1023).
        foldername (str): Nome della cartella in cui salvare il file.
        filename (str): Nome del file BMP da salvare.
    """
    # Creazione della cartella se non esiste
    os.makedirs(foldername, exist_ok=True)

    # Creazione della mappa di grigi alternata
    gray_map = np.zeros((height, width), dtype=np.uint16)
    for x in range(width):
        gray_map[:, x] = value1 if (x // period) % 2 == 0 else value2

    # Conversione al formato RGB 10-bit
    img_rgb = graylevel_to_rgb10bit(gray_map)

    # Salvataggio in BMP
    filepath = os.path.join(foldername, filename)
    Image.fromarray(img_rgb, 'RGB').save(filepath)


#%% Parametri di generazione grating
width = 1920
height = 1200
period = 5

# Range di livelli di grigio (0-1023)
g1 =0  # Valore iniziale del grigio
foldername = f"Calibration_gratings_{width}x{height}_period{period}px_{g1}to1023"

# Generazione delle immagini di calibrazione
for i in tqdm(range(1024 - g1)):
    create_striped_bmp_10bit(width, height, period, i + g1, g1, foldername, f"grating_{width}x{height}_period{period}_{i:04d}.bmp")

#%%Genera checkerboard
def create_binary_checkerboard(width, height, square_size, value1=1023, value2=0, foldername="Binary_Checkerboard", filename="checkerboard.bmp"):
    """
    Crea un'immagine BMP con un checkerboard binario (solo due livelli di grigio).

    Args:
        width (int): Larghezza dell'immagine.
        height (int): Altezza dell'immagine.
        square_size (int): Dimensione dei quadrati (in pixel).
        value1 (int): Livello di grigio per i quadrati chiari (default: 1023).
        value2 (int): Livello di grigio per i quadrati scuri (default: 0).
        foldername (str): Nome della cartella in cui salvare il file.
        filename (str): Nome del file BMP da salvare.
    """
    # Creazione della cartella se non esiste
    os.makedirs(foldername, exist_ok=True)

    # Creazione della mappa checkerboard
    gray_map = np.zeros((height, width), dtype=np.uint16)
    for y in range(height):
        for x in range(width):
            gray_map[y, x] = value1 if ((x // square_size) + (y // square_size)) % 2 == 0 else value2

    # Conversione al formato RGB 10-bit
    img_rgb = graylevel_to_rgb10bit(gray_map)

    # Salvataggio in BMP
    filepath = os.path.join(foldername, filename)
    Image.fromarray(img_rgb, 'RGB').save(filepath)

    print(f"Checkerboard salvato in {filepath}")

# width = 1920
# height = 1200
# square_size = 50  # Dimensione dei quadrati in pixel

# # Genera un checkerboard binario e lo salva
# create_binary_checkerboard(width, height, square_size)  
