# -*- coding: utf-8 -*-
"""
RGB Phase Measurement Function with Adjustable Parameters
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks

def inverse(I, off, amp):
    phase = 2 * np.arccos(np.sqrt((I - off) / amp))
    return phase

def phase_measurement(file_name, savgol_window=25, savgol_poly=2, max_index=-1, title="Phase Measurement"):
    """
    Measures and plots the phase and intensity relationship for a calibrated RGB file.
    
    Parameters:
    - file_name: str, path to the .npy file to load, representing Intensity measurements
    - savgol_window: int, window size for the Savitzky-Golay filter (default: 25).
    - savgol_poly: int, polynomial order for the Savitzky-Golay filter (default: 2).
    - max_index: int, index to be used in the correction calculation (default: -1, the last index).
    - title: str, title for the plot (default: "Phase Measurement").
    
    The function plots three graphs in a single figure:
    1. The raw and smoothed intensity measurements for comparison.
    2. The normalized and scaled intensity measurements.
    3. The phase vs. gray levels after calibration, with an indication of the 2π modulation cutoff.
    """
    # Load the selected file
    ints_m = np.load(file_name)

    # Upsample and apply Savitzky-Golay filter
    graylevels = np.linspace(0, 255, 256)
    graylevels_upsampled = np.linspace(0, 255, 1000)
    ints_smoothed = np.interp(graylevels_upsampled, graylevels, savgol_filter(ints_m, savgol_window, savgol_poly))

    # Normalize intensity
    ints_normalized = (ints_smoothed - np.min(ints_smoothed)) / (np.max(ints_smoothed) - np.min(ints_smoothed))

    # Rescale for absorption effects
    peakposition, _ = find_peaks(ints_smoothed)
    peakvalue = ints_smoothed[peakposition]
    correction = ints_smoothed[0] - np.linspace(0, 1000, 1000) * (ints_smoothed[0] - peakvalue[max_index]) / peakposition[max_index]
    norm_1 = ints_smoothed / correction

    # Convert intensity to phase
    offset_m = np.min(norm_1)
    amplitude_m = np.max(norm_1) - offset_m
    phase_0 = inverse(norm_1, offset_m, amplitude_m)

    # Resolve phase discontinuities
    phase = phase_0
    inversion_position = np.argmax(phase)
    phase[inversion_position:] = 2 * np.pi - phase[inversion_position:]

    # Find cutoff value
    peaks_phase, _ = find_peaks(phase)
    x_peaks = graylevels_upsampled[peaks_phase]
    cutoff = round(x_peaks[-1])

    # Plotting
    fig, axs = plt.subplots(3, 1, figsize=(10, 12))
    fig.suptitle(title, fontsize=16, fontweight='bold')

    # Subplot 1: Raw vs Smoothed Intensity
    axs[0].plot(graylevels, ints_m, label='Raw Intensity', color='blue')
    axs[0].plot(graylevels_upsampled, ints_smoothed, label='Smoothed Intensity (Savitzky-Golay)', color='red')
    axs[0].set_xlabel('Gray Level')
    axs[0].set_ylabel('Intensity [p.u.]')
    axs[0].legend()
    axs[0].set_title('Raw vs Smoothed Intensity')

    # Subplot 2: Normalized and Scaled Intensity
    axs[1].plot(graylevels_upsampled, ints_normalized, label='Intensity measured, normalized')
    axs[1].plot(graylevels_upsampled, (norm_1 - offset_m) / amplitude_m, label='Intensity measured, normalized + scaled')
    axs[1].set_xlabel('Gray Level')
    axs[1].set_ylabel('Intensity [p.u.]')
    axs[1].legend()
    axs[1].set_title('Normalized and Scaled Intensity')

    # Subplot 3: Phase plot
    axs[2].plot(graylevels_upsampled, phase, label='Phase vs Graylevels')
    axs[2].set_title("Phase vs Graylevels after calibration")
    axs[2].set_xlabel('Gray Level')
    axs[2].set_ylabel('Phase')
    axs[2].axvline(x=cutoff, color='black', linestyle='--', label=f'2π modulation at {cutoff}')
    axs[2].legend()

    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to make room for the title
    plt.show()

# Usage
phase_measurement('int_measured_red_calibrated.npy', savgol_window=20, savgol_poly=2, max_index=-1, title="Red_ calibrated - Phase Measurement")
phase_measurement('int_measured_green_calibrated.npy', savgol_window=25, savgol_poly=2, max_index=-1, title="Green - Phase Measurement")
phase_measurement('int_measured_blue_calibrated.npy', savgol_window=30, savgol_poly=2, max_index=-1, title="Blue - Phase Measurement")
