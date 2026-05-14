# -*- coding: utf-8 -*-
"""
Analisi della risposta dell'SLM Santec e generazione della LUT di correzione.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks
from scipy.interpolate import interp1d


def inverse(I, off, amp):
    """Converti intensità in fase."""
    return 2 * np.arccos(np.sqrt((I - off) / amp))


def compute_lut(file_name, upsampling=10000, savgol_window=25, savgol_poly=2, max_index=-1, title="LUT Computation"):
    """
    Calcola la LUT di correzione per l'SLM Santec a partire dai dati misurati.

    Args:
        file_name (str): Percorso del file .npy con le misure di intensità.
        upsampling (int): Numero di punti per l'upsampling (default: 10000).
        savgol_window (int): Finestra per il filtro Savitzky-Golay.
        savgol_poly (int): Ordine del polinomio per il filtro.
        max_index (int): Indice per il valore massimo di correzione.
        title (str): Titolo del grafico.

    Returns:
        function: Funzione di interpolazione LUT (gray_corrected = lut(gray_original)).
    """

    # Carica il file contenente i dati di intensità misurata
    ints_m = np.load(file_name)
    
    # Definiamo i livelli di grigio (ora da 0 a 1023)
    graylevels = np.linspace(0, 1023, 1024)
    graylevels_upsampled = np.linspace(0, 1023, upsampling)  # Parametro upsampling

    # Applica il filtro di Savitzky-Golay per ridurre il rumore
    ints_smoothed = np.interp(
        graylevels_upsampled, graylevels, savgol_filter(ints_m, savgol_window, savgol_poly)
    )

    # Normalizza l'intensità
    ints_normalized = (ints_smoothed - np.min(ints_smoothed)) / (np.max(ints_smoothed) - np.min(ints_smoothed))

    # Correggi per effetti di assorbimento
    peakposition, _ = find_peaks(ints_smoothed)
    peakvalue = ints_smoothed[peakposition]
    correction = ints_smoothed[0] - np.linspace(0, upsampling - 1, upsampling) * (ints_smoothed[0] - peakvalue[max_index]) / peakposition[max_index]
    norm_1 = ints_smoothed / correction

    # Converti intensità in fase
    offset_m = np.min(norm_1)
    amplitude_m = np.max(norm_1) - offset_m
    phase_0 = inverse(norm_1, offset_m, amplitude_m)

    # Risolvi discontinuità della fase
    phase = phase_0
    inversion_position = np.argmax(phase)
    phase[inversion_position:] = 2 * np.pi - phase[inversion_position:]

    # Trova il punto di taglio della modulazione 2π
    peaks_phase, _ = find_peaks(phase)
    x_peaks = graylevels_upsampled[peaks_phase]
    cutoff = round(x_peaks[-1])

    # Costruzione della LUT
    lut = interp1d(phase, graylevels_upsampled, kind="linear", fill_value="extrapolate")

    # Plot dei risultati
    fig, axs = plt.subplots(3, 1, figsize=(10, 12))
    fig.suptitle(title, fontsize=16, fontweight='bold')

    # Subplot 1: Intensità originale vs smoothed
    axs[0].plot(graylevels, ints_m, label='Raw Intensity', color='blue')
    axs[0].plot(graylevels_upsampled, ints_smoothed, label='Smoothed Intensity (Savitzky-Golay)', color='red')
    axs[0].set_xlabel('Gray Level (0-1023)')
    axs[0].set_ylabel('Intensity [p.u.]')
    axs[0].legend()
    axs[0].set_title('Raw vs Smoothed Intensity of Zero Order ')

    # Subplot 2: Normalized and Scaled Intensity
    axs[1].plot(graylevels_upsampled, ints_normalized, label='Normalized Intensity')
    axs[1].plot(graylevels_upsampled, (norm_1 - offset_m) / amplitude_m, label='Scaled Intensity')
    axs[1].set_xlabel('Gray Level (0-1023)')
    axs[1].set_ylabel('Intensity [p.u.]')
    axs[1].legend()
    axs[1].set_title('Normalized and Scaled Intensity')

    # Subplot 3: LUT - Gray Corrected vs Gray Original
    gray_corrected = lut(phase)
    axs[2].plot(phase, gray_corrected, label='Corrected Gray Level')
    axs[2].set_title("LUT: Gray Level Correction")
    axs[2].set_xlabel('Phase [radians]')
    axs[2].set_ylabel('Corrected Gray Level (0-1023)')
    axs[2].axvline(x=2 * np.pi, color='black', linestyle='--', label='2π Modulation')
    axs[2].legend()

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

    return lut, graylevels_upsampled, cutoff


# --- Generazione della LUT con upsampling personalizzabile ---
lut, graylevels_upsampled, cutoff = compute_lut('int_measured_450nm_0order_20250311_3.npy', upsampling=10000, savgol_window=100, savgol_poly=2, max_index=-1, title="Phase measured from zero order intensity")


np.save("lut.npy", lut(graylevels_upsampled));