--- CALIBRAZIONE SLM ---
create_calibration_gratings.py 
	Crea una cartella di BMP con grating di periodicità variabile con valori x 0 con x che va da g1 a 255
display_calibration_gratings.py
	Li mostra sull'SLM usando pygame
HOLOEYE PLUTO-2.1 Configuration Manager 2.2.0 (32 bit)
	Va caricata la look up table relativa alla più lunga delle lunghezze d'onda, eccedendo 2pi, regolando i voltaggi di conseguenza
calibration_measurement.py
	misura l'intensità dell'ordine zero in camera al variare del grating
phase_measurement.py
	restituisce fase al variare del graylevel
	a causa di problemi vari(appofondire), il tipo di inversione che faccimamo non ci fa arrivare a 2 pi.
	possiamo procedere quindi a step.
phase_measurement_pt2.py
	Congiunge due misure, una fino a g1 e una da g1+1 alla fine dei graylevels
HOLOEYE PLUTO-2.1 Configuration Manager 2.2.0 (32 bit)
	Caricare look up table 