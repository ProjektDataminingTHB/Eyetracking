import pandas as pd
import numpy as np
import os
from config import Config as cfg
import tools as tls

# Ausführung

verzeichnis = cfg.datenZerlegungHome
dateinamen = os.listdir(verzeichnis)

header_target = ['t_tracker', 'pix_x', 'pix_y']

for dateiname in dateinamen:
    vp_verzeichnisse = verzeichnis + "/" + dateiname
    dateinamen2 = os.listdir(vp_verzeichnisse)

    # Daten auslesen aus der csv-Datei
    target_csv = dateinamen2.pop(dateinamen2.index(dateiname + '.csv'))
    csv_df = pd.read_csv(vp_verzeichnisse + "/" + target_csv, sep=',')
    ziel_zeitstempel = list(csv_df['t_tracker'])
    ziel_zeitstempel = list(ziel_zeitstempel[1:])
    for dateiname2 in dateinamen2:
        task_verzeichnisse = vp_verzeichnisse + "/" + dateiname2
        dateinamen3 = os.listdir(task_verzeichnisse)
        for dateiname3 in dateinamen3:
            messung_verzeichnisse = task_verzeichnisse + "/" + dateiname3
            dateinamen4 = os.listdir(messung_verzeichnisse)
            for dateiname4 in dateinamen4:
                cycle_verzeichnisse = messung_verzeichnisse + "/" + dateiname4
                dateinamen5 = os.listdir(cycle_verzeichnisse)
                for dateiname5 in dateinamen5:
                    messungen_csv = cycle_verzeichnisse + "/" + dateiname5
                    messung_zeitstempel = list(pd.read_csv(messungen_csv, sep=',')['zeitstempel'])
                    messung_zeitstempel = list(messung_zeitstempel[1:])
                    erster_zeitwert = messung_zeitstempel[0]
                    # das entfernt zwar den letzten Punkt in der Liste, allerdings benötigen wir die Liste auch nicht weiter
                    letzter_zeitwert = messung_zeitstempel.pop()
                    erster_wert = tls.finde_ersten_wert(ziel_zeitstempel, erster_zeitwert)
                    letzter_wert = tls.finde_letzten_wert(ziel_zeitstempel, letzter_zeitwert, erster_wert)
                    ergebnis_spalte1 = list(csv_df['t_tracker'])
                    ergebnis_spalte2 = list(csv_df['pix_x'])
                    ergebnis_spalte3 = list(csv_df['pix_y'])

                    beginn = ergebnis_spalte1.index(erster_wert)
                    ende = ergebnis_spalte1.index(letzter_wert) + 1

                    ergebnis_spalte1 = list(ergebnis_spalte1[beginn:ende])
                    ergebnis_spalte2 = list(ergebnis_spalte2[beginn:ende])
                    ergebnis_spalte3 = list(ergebnis_spalte3[beginn:ende])

                    data = np.concatenate((np.array([ergebnis_spalte1]).T,
                                           np.array([ergebnis_spalte2]).T,
                                           np.array([ergebnis_spalte3]).T), axis=1)
                    df = pd.DataFrame(data, columns=header_target)
                    df.to_csv(messung_verzeichnisse + '/' + target_csv, index=False)