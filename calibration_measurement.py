# -*- coding: utf-8 -*-
"""
Misura l'intensità del'ordine zero al variare del grating mostrato sull slm
del tipo 0 graylevel 0 graylevel 0 graylevel 0 
@author: astam
"""

import pco
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.patches import Rectangle

# import pygame
import time
# from screeninfo import get_monitors
# import os
from tqdm import tqdm

from display_calibration_gratings import *

def roi(reference_img, side):
    # Define ROI centered on maximum intensity with side=side
    max_y, max_x = np.unravel_index(np.argmax(reference_img, axis=None), reference_img.shape)
    x1 = max_x - side // 2
    y1 = max_y - side // 2
    x2 = x1 + side
    y2 = y1 + side
    return x1, y1, x2, y2


screen_index=1
folder=r"C:\Users\astam\Desktop\Repositories\holography_astarita\SLM Calibration\calibration_gratings_1920x1080_period20px_0to255"
filename="\grating_1920x1080_period20_"
saved_measure_name='int_measured_red_calibrated_5.npy'

exp_time = 550*1e-6 #[s]


#%% --------- Reference img ----------

#Show First Grating (all black)
index=f"{0:04d}.bmp"
imgpath = folder + filename + index

window = init_pygame(screen_index);    
display_bmp_hologram(imgpath, window)

#Acquire mean from 5 imgs
with pco.Camera() as cam:
    # Capture a new image
    cam.configuration = {'exposure time':exp_time }
    cam.record(number_of_images=5, mode="sequence")
    images, meta = cam.images()
    reference_img= np.mean(images, axis=0) # Calcola la media delle immagini acquisite

side=40
x1, y1, x2, y2 = roi(reference_img, side)
plt.imshow(reference_img)
rect = plt.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=1, edgecolor='r', facecolor='none')
plt.gca().add_patch(rect)
print ("Intensità massima nel rettangolino è %d" % np.max(reference_img[y1:y2, x1:x2]) )

#%% --------- Measurement ----------
# Display bmp grating - acquire img- mediate intensity on roi
int_measured = np.zeros(256);
frames=np.zeros((side,side,256));
g1=0
with pco.Camera() as cam:
    cam.configuration = {'exposure time':exp_time }
    for i in tqdm(range (256-g1)) :
        #Display img
        index = f"{i:04d}.bmp"
        imgpath = folder + filename + index
        display_bmp_hologram(imgpath, window)
        time.sleep(0.2) 
        
        # Capture a new image as mean of 5
        cam.record(number_of_images=3, mode="sequence")
        images, meta = cam.images()
        img = np.mean(images, axis=0) # Calcola la media delle immagini acquisite
        img = img[y1:y2, x1:x2]
        frames[:,:,i]=img
        int_measured[i]=np.sum(img);
        time.sleep(0.2)

close_pygame()

np.save(saved_measure_name, int_measured)
