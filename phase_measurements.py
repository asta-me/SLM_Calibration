# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 18:15:58 2024

@author: astam
"""

import numpy as np 
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

def inverse(I, off, amp):
    phase = 2 * np.arccos( np.sqrt((I - off) / amp) )
    # phase = np.arccos(2*(I-off)/amp-1)
    return phase


#%% --------- Measurement ----------
#importo intensità misurate
# ints_m= np.load('int_measured_calib_2pi.npy')
ints_m= np.load('int_measured_red_2pi_calibrated.npy')

#Sovracampiono
graylevels = np.linspace(0, 255, 256)
graylevels_upsampled = np.linspace(0, 255, 1000)
ints = np.interp( graylevels_upsampled, graylevels, savgol_filter(ints_m, 20, 2));

#Estraggo offset e Ampiezza di riscalamento
offset_m = np.min(ints)
amplitude_m = np.max(ints) - offset_m

#Ricavo fase con funzione inversa
phase_0 = inverse(ints, offset_m, amplitude_m)
plt.figure();
plt.xlabel('Gray Level'); plt.ylabel('Phase')
plt.title('Phase vs GrayLevels Upsampled')  # Optionally add a title
plt.plot(graylevels_upsampled, phase_0)

# Risolvo discontnuità di fase
phase = phase_0
inversion_position = np.argmax(phase);
phase[inversion_position:] = 2 * np.pi - phase[inversion_position:]

#Downsampling per riportare alle dimensioni che mi servono
phase_1 = np.interp( graylevels, graylevels_upsampled, phase);

#%% LUT da caricare sull'SLM
plt.figure()
plt.title("LUT phase vs Graylevels")  # Optionally add a title
plt.xlabel('Gray Level'); plt.ylabel('Phase')
plt.plot(graylevels, phase_1)
plt.plot(graylevels_upsampled, phase_0)

# %% Dataset Creation
# Vmin=0; Vmax=1;
# volts = np.linspace(Vmin, Vmax, 255)
# volts_upsampled = np.linspace(Vmin, Vmax, 1000)
# phase = np.linspace(0, 2.2*np.pi, 255)
# offset = 3; I0 = 5;
# eta_0 = np.cos(phase/2)**2
# # eta_0 = 0.5* (1+ np.cos(phase))
# i_0 = offset + I0*eta_0
# noise = np.random.normal(0, 0.1, i_0.shape)  # Genera rumore con media 0 e deviazione standard 0.1
# ints_m = i_0 + noise # _m means measured

