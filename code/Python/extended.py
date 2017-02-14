import pandas as pd
import numpy as np
import os
from config import Config as cfg
import tools as tls
import ntpath
from shutil import copyfile
import math

def berechne_Geschwindigkeit(y, x, t):
    y_values = y.values
    x_values = x.values
    t_values = t.values
    ergebnis = list()
    x1 = 0.0
    y1 = 0.0
    t1 = 0.0
    rechnen = False
    for i in range(len(t.values)):
        # Berechnung der Zeitstempeldifferenz, die nicht 0 sein darf, wegen der Division
        dif_t = t1 - t_values[i]
        # Kriterien, wann gerechnet werden darf:
        # es muessen gueltige Werte vorliegen, also keine 0 bei den Blickdaten
        # die Division muss moeglich sein
        if int(x1) != 0 and int(y1) != 0 and dif_t != 0:
            rechnen = True
        else:
            rechnen = False
        if rechnen:
            dif_x = x1 - x_values[i]
            dif_y = y1 - y_values[i]
            ergebnis.append(math.sqrt(math.pow(dif_x, 2) + math.pow(dif_y, 2)) / math.pow(dif_t, 2))
        else:
            ergebnis.append(0)
        x1 = x_values[i]
        y1 = y_values[i]
        t1 = t_values[i]
    return ergebnis

def berechne_Abweichungsrichtung(start_target, aktuell_target, blick):
    # Da der erste Wert bei der Differenzbildung immer weitergehen muss, hier die Wertuebergabe
    wert1 = start_target
    akt_values = aktuell_target.values
    blick_values = blick.values
    ergebnis = list()
    for i in range(len(akt_values)):
        richtung = int((wert1 - akt_values[i]) * 1000)
    # Fall1:    Die Bewegung geht in Richtung aufsteigende Werte
    #           Der Blick ist vor dem Ziel
        if (richtung < 0) and (akt_values[i] < blick_values[i]):
            ergebnis.append(1)
    # Fall2:    Die Bewegung geht in Richtung absteigende Werte
    #           Der Blick ist hinter dem Ziel
        if (richtung > 0) and (akt_values[i] < blick_values[i]):
            ergebnis.append(-1)
    # Fall3:    Die Bewegug geht in Richtung aufsteigende Werte
    #           Der Blick ist hinter dem Ziel
        if (richtung < 0) and (akt_values[i] > blick_values[i]):
            ergebnis.append(-1)
    # Fall4:    Die Bewegung geht in Richtung absteigende Werte
    #           Der Blick ist vor dem Ziel
        if (richtung > 0) and (akt_values[i] > blick_values[i]):
            ergebnis.append(1)
    # Fall5:    Die richtung ist 0 --> Der Targetwert aendert sich nicht --> dadurch ist es egal, wie sich der Blickwert aendert --> Ergebnis ist 0
        if richtung == 0:
            ergebnis.append(0)

    # Umsetzen des startpunktes
        wert1 = akt_values[i]
    return ergebnis


def extend_files():
    header_source = ['t_tracker', 'pix_x', 'pix_y', 'zeitstempel', 'blick_l_x', 'blick_l_y', 'blick_r_x', 'blick_r_y']
    source_folders = os.listdir(cfg.matchedHome)
    for folder in source_folders:
        if os.path.exists(os.path.join(cfg.extendedHome, folder)) == False:
            os.makedirs(os.path.join(cfg.extendedHome, folder))

        source_path = os.path.join(cfg.matchedHome, folder)
        destination_path = os.path.join(cfg.extendedHome, folder)
        source_file_list = os.listdir(source_path)

        for source_file in source_file_list:
            #Die Dateien mit den Informationen zu der Anzahl der Datensaetze pro Versuch werden genauso uebernommen, wie sie sind
            if 'stats' in source_file:
                copyfile(os.path.join(source_path, source_file), os.path.join(destination_path, source_file))
            #Die Dateien mit den gematchten Daten werden erweitert, um neue Datenreihen
            else:
                source = pd.read_csv(os.path.join(source_path, source_file), sep=',', names = header_source).ix[1:]
                #Erweiterung um die Mittelposition der Blickwerte der Augen
                middle_eyes = source.assign(blick_m_x = pd.to_numeric(source.blick_l_x) / 2 + pd.to_numeric(source.blick_r_x) / 2, blick_m_y = pd.to_numeric(source.blick_l_y) / 2 + pd.to_numeric(source.blick_r_y) / 2, pix_x_translation = pd.to_numeric(source.pix_x).add(640), pix_y_translation = (pd.to_numeric(source.pix_y) * -1).add(512))

                # Erweiterung um die Werte der Distanz der Blickposition zur Targetposition
                distanz = middle_eyes.assign(delta_l_t = lambda x : np.sqrt(np.power(pd.to_numeric(x.blick_l_x) - pd.to_numeric(x.pix_x_translation),2) + np.power(pd.to_numeric(x.blick_l_y) - pd.to_numeric(x.pix_y_translation),2)), delta_r_t = lambda x : np.sqrt(np.power(pd.to_numeric(x.blick_r_x) - pd.to_numeric(x.pix_x_translation),2) + np.power(pd.to_numeric(x.blick_r_y) - pd.to_numeric(x.pix_y_translation),2)), delta_m_t = lambda x : np.sqrt(np.power(pd.to_numeric(x.blick_m_x) - pd.to_numeric(x.pix_x_translation),2) + np.power(pd.to_numeric(x.blick_m_y) - pd.to_numeric(x.pix_y_translation),2)))

                # Erweiterung um die Geschwindigkeiten
                geschwindigkeit = distanz.assign(geschwindigkeit_l = berechne_Geschwindigkeit(pd.to_numeric(distanz.blick_l_y), pd.to_numeric(distanz.blick_l_x), pd.to_numeric(distanz.zeitstempel)), geschwindigkeit_r = berechne_Geschwindigkeit(pd.to_numeric(distanz.blick_r_y), pd.to_numeric(distanz.blick_r_x), pd.to_numeric(distanz.zeitstempel)), geschwindigkeit_m = berechne_Geschwindigkeit(pd.to_numeric(distanz.blick_m_y), pd.to_numeric(distanz.blick_m_x), pd.to_numeric(distanz.zeitstempel)))

                #Berechnung, ob die Blickposition hinterher ist, oder voraus.
                # 1 = voraus
                # -1 = hinterher
                # 0 = Keine Aenderung in Zielwert (Betrifft y-Position in Versuch: horizontal)
                start_x = 640.0
                start_y = 512.0
                result = geschwindigkeit.assign(richtung_delta_l_x = berechne_Abweichungsrichtung(start_x, pd.to_numeric(distanz.pix_x_translation), pd.to_numeric(distanz.blick_l_x)), richtung_delta_r_x = berechne_Abweichungsrichtung(start_x, pd.to_numeric(distanz.pix_x_translation), pd.to_numeric(distanz.blick_r_x)), richtung_delta_l_y = berechne_Abweichungsrichtung(start_y, pd.to_numeric(distanz.pix_y_translation), pd.to_numeric(distanz.blick_l_y)), richtung_delta_r_y = berechne_Abweichungsrichtung(start_y, pd.to_numeric(distanz.pix_y_translation), pd.to_numeric(distanz.blick_r_y)), richtung_delta_m_x = berechne_Abweichungsrichtung(start_x, pd.to_numeric(distanz.pix_x_translation), pd.to_numeric(distanz.blick_m_x)), richtung_delta_m_y = berechne_Abweichungsrichtung(start_y, pd.to_numeric(distanz.pix_y_translation), pd.to_numeric(distanz.blick_m_y)))

                # Ergebnis in CSV-Datei schreiben
                result.to_csv(os.path.join(destination_path, source_file), index=False)

extend_files()
