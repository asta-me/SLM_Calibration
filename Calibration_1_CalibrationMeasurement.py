"""
Misura l'intensit√† dell'ordine zero al variare del grating mostrato sull'SLM Santec.
"""

import numpy as np
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
from pygame_functions import *  
# from camera_control import *

from vimba import Vimba

def open_camera():
    """ Opens the camera once and returns the camera object. """
    vimba = Vimba.get_instance()
    vimba.__enter__()  # Simulate "with" to keep Vimba open
    cam = vimba.get_all_cameras()[0]
    cam.__enter__()  # Simulate "with" to keep the camera open
    return vimba, cam

def close_camera(vimba, cam):
    """ Closes the camera and releases resources. """
    cam.__exit__(None, None, None)  # Close the camera
    vimba.__exit__(None, None, None)  # Close Vimba

def acquire_image(cam):
    """ Acquire a single frame and return it as a 2D NumPy array. """
    return cam.get_frame().as_numpy_ndarray().squeeze()

def acquire_average_image(cam, num_frames=5):
    """ Acquire multiple frames and return their mean as a 2D NumPy array. """
    frames = [acquire_image(cam) for _ in range(num_frames)]
    return np.mean(frames, axis=0)

def set_parameters(cam, exposure: float = None, gain: float = 1):
    """ Set exposure time (µs) and gain (dB) on an already opened camera. """
    if exposure is not None:
        cam.get_feature_by_name("ExposureTime").set(exposure)
    if gain is not None:
        cam.get_feature_by_name("Gain").set(gain)


def roi(reference_img, side=40):
    """
    Definisce la ROI centrata sulla massima intensit√†.

    Args:
        reference_img (numpy.ndarray): Immagine di riferimento.
        side (int): Dimensione della ROI quadrata.

    Returns:
        tuple: Coordinate della ROI (x1, y1, x2, y2).
    """
    max_y, max_x = np.unravel_index(np.argmax(reference_img, axis=None), reference_img.shape)
    x1, y1 = max_x - side // 2, max_y - side // 2
    x2, y2 = x1 + side, y1 + side
    return x1, y1, x2, y2


#%% --- PARAMETERS ---
screen_index = 1
folder = r"C:\Users\astam\Desktop\Repositories\holography_astarita\Cambridge\Calibration_gratings_1920x1200_period5px_0to1023"
filename = r"\grating_1920x1200_period5_"
saved_measure_name = 'int_measured_450nm_0order_20250311_3.npy'

exp_time = 30.091  # Exposure time in µs
exp_time = 70.091  # Exposure time in µs
# exp_time = 350.091  # Exposure time in µs

#%% --- REFERENCE IMAGE ---
#%% Show the first grating (completely black) and acquire reference image
index = f"{1000:04d}.bmp"
imgpath = folder + filename + index
window = init_pygame(screen_index)
display_bmp_hologram(imgpath, window)

#%% Acquire calib measurement
# Open camera once
vimba, cam = open_camera()
set_parameters(cam, exposure=exp_time, gain=1)  # Set exposure time and gain

reference_img = acquire_average_image(cam, num_frames=5)  # Acquire reference
close_camera(vimba, cam)  # Close camera properly
# Determine ROI
x1, y1, x2, y2 = roi(reference_img, side=40)
plt.imshow(reference_img)
rect = plt.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=1, edgecolor='r', facecolor='none')
plt.gca().add_patch(rect)
print(f"Maximum intensity in ROI: {np.max(reference_img[y1:y2, x1:x2])}")


#%% --- MEASUREMENT ---

vimba, cam = open_camera()
int_measured = np.zeros(1024)

for i in tqdm(range(1024)):
    # Show current grating on SLM
    index = f"{i:04d}.bmp"
    imgpath = folder + filename + index
    display_bmp_hologram(imgpath, window)
    time.sleep(0.1)  # Reduced delay

    # Acquire image
    img = acquire_average_image(cam, num_frames=5)
    img = img[y1:y2, x1:x2]  # Apply ROI
    int_measured[i] = np.sum(img)

close_pygame()
close_camera(vimba, cam)  # Close camera properly

#%% Save results
np.save(saved_measure_name, int_measured)
