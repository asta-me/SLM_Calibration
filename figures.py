# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 10:36:38 2024
Figure relative alla calibrazione RGB

@author: astam

"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from scipy.signal import find_peaks

i_r_before = np.load('int_measured_calib_2pi_red.npy');
i_r = np.load('int_measured_red_2pi_calibrated.npy');
i_g = np.load('int_measured_green.npy');
i_b = np.load('int_measured_blue.npy');

#Sovracampiono
gl = np.linspace(0, 255, 256)
gl_upsampled = np.linspace(0, 255, 1000)
i_r_before_clean = np.interp( gl_upsampled, gl, savgol_filter(i_r_before, 20, 2));
i_r_clean = np.interp( gl_upsampled, gl, savgol_filter(i_r, 20, 2));
i_g_clean = np.interp( gl_upsampled, gl, savgol_filter(i_g, 20, 2));
i_b_clean = np.interp( gl_upsampled, gl, savgol_filter(i_b, 20, 2));

#Normalizzo tra 0 e 1
i_r_before_clean = (i_r_before_clean - np.min(i_r_before_clean)) / (np.max(i_r_before_clean) - np.min(i_r_before_clean))
i_r_clean = (i_r_clean - np.min(i_r_clean)) / (np.max(i_r_clean) - np.min(i_r_clean))
i_g_clean = (i_g_clean - np.min(i_g_clean)) / (np.max(i_g_clean) - np.min(i_g_clean))
i_b_clean = (i_b_clean - np.min(i_b_clean)) / (np.max(i_b_clean) - np.min(i_b_clean))


# Find peaks (manual check for the borders)
peaks_g, _ = find_peaks(i_g_clean)
peaks_b, _ = find_peaks(i_b_clean)
if i_g_clean[0] > i_g_clean[1]:
    peaks = np.insert(peaks_g, 0, 0)
if i_g_clean[-1] > i_r_clean[-2]:
    peaks_g = np.append(peaks_g, len(i_g_clean) - 1)
    
if i_b_clean[0] > i_b_clean[1]:
    peaks_b = np.insert(peaks_b, 0, 0)
if i_b_clean[-1] > i_b_clean[-2]:
    peaks_b = np.append(peaks_b, len(i_b_clean) - 1)

# Extract the corresponding x-values and y-values of the peaks
x_peaks_g = gl_upsampled[peaks_g]; y_peaks_g = i_g_clean[peaks_g]
x_peaks_b = gl_upsampled[peaks_b]; y_peaks_b = i_b_clean[peaks_b]

#Cutoff Value is in the second peak
g_cutoff = round(x_peaks_g[1])
b_cutoff = round(x_peaks_b[1])

print(f'Green 2pi modulation at graylevel= {g_cutoff}')
print(f'Blue 2pi modulation at graylevel= {b_cutoff}')

# Plots
plt.figure(1); plt.plot(gl_upsampled,i_r_before_clean, color='red')
plt.title('Intensity of Red Light Before Calibration')
plt.xlabel('Gray Level'); plt.ylabel('Intensity [p.u.]')

plt.figure(2);plt.plot(gl_upsampled,i_r_clean, color='red')
plt.title('Intensity of Red Light After Calibration')
plt.xlabel('Gray Level');plt.ylabel('Intensity [p.u.]')

plt.figure(3);plt.plot(gl_upsampled,i_g_clean, color='green')
plt.plot(x_peaks_g, y_peaks_g, 'kx')  # 'kx' for blk cross
plt.axvline(x=g_cutoff, color='black', linestyle='--', label=f'2pi modulation at {g_cutoff}')
plt.title('Intensity of Green Light After Calibration')
plt.xlabel('Gray Level'); plt.ylabel('Intensity [p.u.]')
plt.legend() 

plt.figure(4);plt.plot(gl_upsampled,i_b_clean, color='blue')
plt.plot(x_peaks_b, y_peaks_b, 'kx')  # 'kx' for blk cross
plt.axvline(x=b_cutoff, color='black', linestyle='--', label=f'2pi modulation at {b_cutoff}')
plt.title('Intensity of Blue Light After Calibration')
plt.xlabel('Gray Level'); plt.ylabel('Intensity [p.u.]')
plt.legend()
