
# SLM_Calibration

Questo repository raccoglie dati e script per la calibrazione di uno Spatial Light Modulator (SLM) a fase pura.

## Descrizione

Contiene metodi, dati sperimentali e script (da rivedere e pulire) utilizzati per la calibrazione di SLM, in particolare:

- **Metodo del grating**: si genera un reticolo (grating) con fase variabile tra 0 e φ, e si misura la risposta del SLM in funzione del livello di grigio applicato. Questo permette di ricostruire la curva di calibrazione fase vs. livello di grigio.
- **Dati sperimentali**: sono inclusi file `.npy` e `.txt` con misure di intensità e fase per diversi canali colore e condizioni di calibrazione.

## File principali

- `create_calibration_gratings.py`: genera i pattern di grating per la calibrazione.
- `display_calibration_gratings.py`: visualizza i grating sullo SLM.
- `calibration_measurement.py`: script per acquisire le misure di intensità.
- `phase_measurements.py`, `phase_measurements_pt2.py`, `phase_measurement_remormalization.py`: analisi delle misure di fase.
- `figures.py`: script per la visualizzazione e l'analisi dei risultati.
- File `.npy` e `.txt`: dati sperimentali raccolti durante le sessioni di calibrazione.

## Note

- Gli script sono da riorganizzare e documentare meglio, ma rappresentano una base funzionante per la calibrazione di SLM.
- Il metodo principale implementato è quello del grating con fase variabile.

---
Per domande o contributi: Marco Astarita
