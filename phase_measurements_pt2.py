# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29  2024

In questa versione v2 voglio provare il metodo a step proposto da paolo, con diverse griglie (2)

1° misura : soddisfacente fino al valore g1.
2° misura : andrà da g1 a 255. avrà 256-g1 elementi.

@author: astam
"""

import numpy as np 
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

def inverse(I, off, amp):
    phase = 2 * np.arccos( np.sqrt((I - off) / amp) )
    # phase = np.arccos(2*(I-off)/amp-1)
    return phase

#%% Inizio estrazione fase
#importo intensità misurate
ints_m = np.load('int_measured_calib_2pi_red.npy')

#Sovracampiono
graylevels = np.linspace(0, ints_m.shape[0]-1, ints_m.shape[0])
graylevels_upsampled = np.linspace(0, ints_m.shape[0]-1, 1000)
ints = np.interp( graylevels_upsampled, graylevels, savgol_filter(ints_m, 20, 2));

#Estraggo offset e Ampiezza di riscalamento
offset_m = np.min(ints)
amplitude_m = np.max(ints) - offset_m

#Ricavo fase con funzione inversa
phase_0 = inverse(ints, offset_m, amplitude_m)
plt.figure("1");plt.title("Phase vs GrayLevels Upsampled (red) (misura 1)")
plt.plot(graylevels_upsampled, phase_0)
plt.xlabel('Gray Level'); plt.ylabel('Phase')


# Risolvo discontnuità di fase dovute all'inversione del coseno
phase = phase_0
inversion_position = np.argmax(phase);
phase[inversion_position:] = 2 * np.pi - phase[inversion_position:]

#Downsampling per riportare alle dimensioni che mi servono
phase_1 = np.interp( graylevels, graylevels_upsampled, phase);
plt.figure("2");plt.title("Phase vs GrayLevels Upsampled (red) (misura 1) pi inverted")
plt.plot(graylevels, phase_1)
plt.xlabel('Gray Level'); plt.ylabel('Phase')



#%% LUT da caricare sull'SLM
# plt.figure("NUMERO");plt.title("LUT phase vs Graylevels")
# plt.plot(graylevels, phase_1)


#%%--------- 2° Misura --------------
# Vogliamo ricavare dalla prima misura la fase corrispettiva ai graylevels 0 - g1
# Nella seconda misura ci interessa ricavare la fase relativa ai graylevels g1+1 - 255 
#Per saltare

# g1 è il valore di GL dopo il quale prendiamo la seconda misura. Questo valore è scelto 
# a mano considerando phase2_1(gl) e si prende un valore ragionevole dopo il quale la linearità è buona
# g1 > g1-overlap per cui overlap > 0
# overlap corrisponde ai valori iniziali scartati dalla seconda misura che vengono anche presi alla fine della prima misura.
# g1-overlap rappresenta il valore gl di inizio della seconda misura.

g1=150
overlap = 20
m2_iv = g1 - overlap # valore iniziale seconda misura
ints_m2= np.load('int_measured_calib_2pi_red_2.npy')
ints_m2= ints_m2 [0:(256-(m2_iv))];

#Sovracampiono
graylevels2 = np.linspace((m2_iv), 255, 256 - (m2_iv))
graylevels_upsampled2 = np.linspace((m2_iv), 255, 1000)
ints2 = np.interp( graylevels_upsampled2, graylevels2, savgol_filter(ints_m2, 20, 2));

#Estraggo offset e Ampiezza di riscalamento
offset_m2 = np.min(ints2)
amplitude_m2 = np.max(ints2) - offset_m2

#Ricavo fase con funzione inversa
phase2_0 = inverse(ints2, offset_m2, amplitude_m2)
plt.figure("3");plt.title("Phase vs GrayLevels Upsampled (red) (misura2)")
plt.plot(graylevels_upsampled2, phase2_0)
plt.xlabel('Gray Level'); plt.ylabel('Phase')

# Risolvo discontnuità di fase
phase2 = phase2_0
inversion_position2 = np.argmax(phase2);
phase2[inversion_position2:] = 2 * np.pi - phase2[inversion_position2:]

#Downsampling per riportare alle dimensioni che mi servono
phase2_1 = np.interp( graylevels2, graylevels_upsampled2, phase2);

#%% LUT da caricare sull'SLM
plt.figure("4");plt.title("Phase vs Graylevels pi inverted (misura2)")
plt.plot(graylevels2, phase2_1)
plt.xlabel('Gray Level'); plt.ylabel('Phase')


#%% Unione di phase1 e phase2_1
total_phase = np.append(phase_1[:g1],phase_1[g1]- phase2_1[overlap] + phase2_1[overlap:(256-(m2_iv))])
total_phase = total_phase/np.pi;
# Visualizza l'andamento di Total_phase
plt.figure("5");plt.title("Total Phase vs Graylevels")
plt.plot(np.linspace(0, 255, 256), total_phase)
plt.show()
plt.xlabel('Gray Level'); plt.ylabel('Phase')



#%% Crea un file di testo per la calibrazione, come richiesto dal software holoeye
with open('phase_vs_graylevels.txt', 'w') as file:
    # Scrivi l'intestazione
    file.write("# Measured GL\tPhase [pi rad]:\n")
    # Scrivi i dati
    for gl, phase in zip(graylevels, total_phase):
        file.write(f"{gl}\t{phase:.6f}\n")
