import numpy as np
import matplotlib.pyplot as plt

# Carica la LUT salvata
lut_red = np.load("LUT_red.npy")
lut_green = np.load("LUT_green.npy")
lut_blue = np.load("LUT_blue.npy")

# Crea la funzione di interpolazione per ogni canale
from scipy.interpolate import interp1d
graylevels = np.linspace(0, 1023, 1024)  # I valori di grigio originali
lut_red_interp = interp1d(graylevels, lut_red, kind="linear", fill_value="extrapolate")
lut_green_interp = interp1d(graylevels, lut_green, kind="linear", fill_value="extrapolate")
lut_blue_interp = interp1d(graylevels, lut_blue, kind="linear", fill_value="extrapolate")

# Simuliamo una matrice di input con valori da 0 a 1023
M_original = np.random.randint(0, 1024, size=(1080, 1920))

# Applica la LUT a ogni valore della matrice
M_corrected_red = lut_red_interp(M_original)
M_corrected_green = lut_green_interp(M_original)
M_corrected_blue = lut_blue_interp(M_original)

# Mostriamo un confronto tra immagine originale e corretta
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(M_original, cmap='gray')
plt.title("Immagine Originale (0-1023)")

plt.subplot(1, 2, 2)
plt.imshow(M_corrected_red, cmap='gray')
plt.title("Immagine Correttata con LUT (Red)")

plt.show()
