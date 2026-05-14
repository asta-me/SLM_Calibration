# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 11:20:59 2024

@author: astam
"""


import numpy as np 
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

from scipy.signal import find_peaks


def inverse(I, off, amp):
    phase = 2 * np.arccos( np.sqrt((I - off) / amp) )
    # phase = np.arccos(2*(I-off)/amp-1)
    return phase

#%% --------- Measurement ----------
ints_m= np.load('int_measured_red_calibrated_5.npy')
# ints_m= np.load('int_measured_green_calibrated_2.npy')
# ints_m= np.load('int_measured_blue_calibrated_1.npy')

#Sovracampiono e filtro
graylevels = np.linspace(0, 255, 256)
graylevels_upsampled = np.linspace(0, 255, 1000)
ints = np.interp( graylevels_upsampled, graylevels, savgol_filter(ints_m, 20, 2));

#Normalizzo
ints_normalized = (ints - np.min(ints))/(np.max(ints) - np.min(ints))

#Riscalo per trascurare effetti di assorbimento
peakposition, _ = find_peaks(ints)
peakvalue = ints[peakposition]
correction = ints[0] - np.linspace(0,1000,1000)*(ints[0]-peakvalue[-1])/peakposition[-1];
#indice -1 da controllare, in caso di molti indici. Nel mio caso va bene per r,g,b; 
norm_1=ints/correction;

#Inverto da intensità a fase
offset_m = np.min(norm_1)
amplitude_m = np.max(norm_1) - offset_m
phase_0 =inverse(norm_1,offset_m,amplitude_m)

# Risolvo discontnuità di fase
phase = phase_0
inversion_position = np.argmax(phase);
phase[inversion_position:] = 2 * np.pi - phase[inversion_position:]

#Find Cutoff Value
# Extract the corresponding x-values and y-values of the peaks

peaks_phase, _ = find_peaks(phase)
x_peaks = graylevels_upsampled[peaks_phase]; y_peaks = phase[peaks_phase]
cutoff = round(x_peaks[-1])




#%% Crea un file di testo per la calibrazione, come richiesto dal software holoeye
phase_final = np.interp( graylevels, graylevels_upsampled, phase);
phase_final = phase_final/np.pi
with open('phase_vs_graylevels.txt', 'w') as file:
    # Scrivi l'intestazione
    file.write("# Measured GL\tPhase [pi rad]:\n")
    # Scrivi i dati
    for gl, phasex in zip(graylevels, phase_final):
        file.write(f"{gl}\t{phasex:.6f}\n")

#%%Plot
plt.figure()
plt.plot(graylevels_upsampled,ints_normalized, label='Ints measured, normalized')
plt.plot(graylevels_upsampled,(norm_1-offset_m)/amplitude_m, label='Ints measured normalized + scaled')
plt.xlabel('Gray Level'); plt.ylabel('Intensity [p.u.]')
plt.legend()

plt.figure()
plt.plot(graylevels_upsampled,phase)
plt.title("Phase vs Graylevels after calibration")  # Optionally add a title
plt.xlabel('Gray Level'); plt.ylabel('Phase')
plt.axvline(x=cutoff, color='black', linestyle='--', label=f'2pi modulation at {cutoff}')
plt.legend() 


    