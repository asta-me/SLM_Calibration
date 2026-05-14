# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 11:15:48 2024

@author: astam
"""
import os
import numpy as np
from PIL import Image
from tqdm import tqdm

def create_striped_bmp(width, height, period, value1, value2, foldername, filename):
    # Creazione della cartella se non esiste già
    if not os.path.exists(foldername):
        os.makedirs(foldername)

    # Percorso completo del file
    filepath = os.path.join(foldername, filename)

    # Creazione dell'immagine
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            img_array[y, x] = [value1, value1, value1] if (x // period) % 2 == 0 else [value2, value2, value2]
    Image.fromarray(img_array, 'RGB').save(filepath)

# Esempio d'uso:
width=1920;
height=1080;
period=20;

# Value from which the second measurement starts
g1=130;

for i in tqdm(range(256-g1)):
    create_striped_bmp(width, height, period, i+g1, g1, f"calibration_gratings_{width}x{height}_period{period}px_{g1}to255", f"grating_{width}x{height}_period{period}_{i:04d}.bmp")    
    




