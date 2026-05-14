# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 10:35:21 2024

@author: astam
"""

import pygame
import numpy as np
import os
from tqdm import tqdm

def init_pygame(screen_index = 0):
    from screeninfo import get_monitors
    if get_monitors()[screen_index].is_primary:
        print("Warning, screen is primary")
    #Initialize
    pygame.init()
    # Get width and height of selected screen
    width, height = pygame.display.get_desktop_sizes()[screen_index]
    # Create window
    window = pygame.display.set_mode((width,height), pygame.NOFRAME, display=screen_index)
    return window

def close_pygame():
    pygame.quit()

def display_numpy_hologram(hologram, window):
    # hologram is a numpy array in 0-255
    # window is a pygame window
    slm_size = window.get_size()[1],window.get_size()[0]
    if hologram.shape[0]>slm_size[0] or hologram.shape[1]>slm_size[1]:
        print("The hologram is too big!")
    #Convert to rgb array
    array = np.stack((hologram, hologram, hologram), axis=2)
    # Converte il numpy array in una superficie Pygame
    surf = pygame.surfarray.make_surface(array)
    # Ottieni le dimensioni della superficie
    surf_rect = surf.get_rect()
    #Center the image
    surf_rect.center = window.get_rect().center
    # Disegna la superficie sulla finestra
    window.blit(surf, surf_rect)
    # Update window
    pygame.display.flip()

def display_bmp_hologram(filename, window):
    # filename is a bmp path
    # window is a pygame window
    
    #Fill w black
    # window.fill((0, 0, 0))
    
    #Load bmp hologram
    image = pygame.image.load(filename)
    #Get center coordinates
    window_width, window_height = window.get_size()
    image_width, image_height = image.get_size()
    x = (window_width - image_width) // 2
    y = (window_height - image_height) // 2
    window.blit(image, (x, y))
    # Update window
    pygame.display.flip()

def display_bmp_video(folder_path, framerate, window):
    #filder path is the path of the folder wih all of the bmp frames
    #framerate sets the framerate
    #window is a pygame object
    
    # Ottieni la lista di tutti i file BMP nella cartella
    bmp_files = [f for f in os.listdir(folder_path) if f.endswith('.bmp')]
    # Ordina i file BMP
    bmp_files.sort()
    # Display every video frame
    for i, bmp_file in enumerate(bmp_files):
        # Load bmp hologram
        image = pygame.image.load(os.path.join(folder_path, bmp_file))
        if i == 0:
            window.fill((0, 0, 0))
            # Get center coordinates
            window_width, window_height = window.get_size()
            image_width, image_height = image.get_size()
            x = (window_width - image_width) // 2
            y = (window_height - image_height) // 2
        # Display current frame
        window.blit(image, (x, y))
        # Update window
        pygame.display.flip()
        # Set framerate
        pygame.time.Clock().tick(framerate)

def navigate_bmp_frames(folder_path, window):
    # Ottieni la lista di tutti i file BMP nella cartella
    bmp_files = [f for f in os.listdir(folder_path) if f.endswith('.bmp')]
    # Ordina i file BMP
    bmp_files.sort()

    # Indice corrente per il frame attualmente visualizzato
    current_frame = 0

    # Carica e visualizza il primo frame
    image = pygame.image.load(os.path.join(folder_path, bmp_files[current_frame]))
    window_width, window_height = window.get_size()
    image_width, image_height = image.get_size()
    x = (window_width - image_width) // 2
    y = (window_height - image_height) // 2
    window.blit(image, (x, y))
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # Avanza al frame successivo
                    current_frame = (current_frame + 1) % len(bmp_files)
                elif event.key == pygame.K_LEFT:
                    # Torna al frame precedente
                    current_frame = (current_frame - 1) % len(bmp_files)
                elif event.key == pygame.K_ESCAPE:
                    # Premendo Esc chiudi il programma
                    running = False
                
                # Carica e visualizza il nuovo frame
                image = pygame.image.load(os.path.join(folder_path, bmp_files[current_frame]))
                window.blit(image, (x, y))
                pygame.display.flip()

    pygame.quit()
    

"""Test Funzioni Pygame"""
# screen_index=1
# framerate=30

##Test phase
# phase=np.random.rand(1080,1920)*2*np.pi
# phase*=255/np.pi/2
# phase=phase.astype(int)

#Test the functions

# display_numpy_hologram(phase, window)
# display_bmp_hologram("pentagon_phase_lines_resc_1.bmp", window)
# display_bmp_video(r"C:\Users\astam\Desktop\OneDrive - Politecnico di Milano\Polimi\Astarita_Holography_Data\Nbody_video",framerate,  window)
# navigate_bmp_frames(r"C:\Users\astam\Desktop\OneDrive - Politecnico di Milano\Polimi\Astarita_Holography_Data\Demo\Demo_unscaled", window)

#close_pygame()

if __name__ == "__main__":
    
    """Esecuzione programma"""
    screen_index=1
    framerate=30
    
    window = init_pygame(screen_index);    
    clock = pygame.time.Clock()
    
    folder=r"C:\Users\astam\Desktop\Repositories\holography_astarita\SLM Calibration\calibration_gratings_1920x1080_period20px_0to255"
    filename="\grating_1920x1080_period20_"
    
    # for i in tqdm(range (256)) :    
    #     index=f"{i:04d}.bmp"
    #     imgpath = folder + filename + index
    #     display_bmp_hologram(imgpath, window)
    #     clock.tick(framerate)
    
    import time
    index=f"{250:04d}.bmp"
    imgpath = folder + filename + index
    display_bmp_hologram(imgpath, window)
    time.sleep(100)
    
    
    close_pygame()


