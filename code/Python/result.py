import pandas as pd
import numpy as np
import os
from config import Config as cfg
import tools as tls
import ntpath
from shutil import copyfile
import math

def versuch_auswerten(versuch_werte, versuch_name, header):

    # Werte verarbeitbar machen
    delta_l_values = pd.to_numeric(versuch_werte.delta_l_t).values
    delta_r_values = pd.to_numeric(versuch_werte.delta_r_t).values
    delta_m_values = pd.to_numeric(versuch_werte.delta_m_t).values
    geschwindigkeit_l_values = pd.to_numeric(versuch_werte.geschwindigkeit_l).values
    geschwindigkeit_r_values = pd.to_numeric(versuch_werte.geschwindigkeit_r).values
    geschwindigkeit_m_values = pd.to_numeric(versuch_werte.geschwindigkeit_m).values
    tendenz_l_values = pd.to_numeric(versuch_werte.tendenz_l).values
    tendenz_r_values = pd.to_numeric(versuch_werte.tendenz_r).values
    tendenz_m_values = pd.to_numeric(versuch_werte.tendenz_m).values

    # Mittelkwerte bestimmen
    mean_delta_l = delta_l_values.mean()
    mean_delta_r = delta_r_values.mean()
    mean_delta_m = delta_m_values.mean()
    mean_geschwindigkeit_l = geschwindigkeit_l_values.mean()
    mean_geschwindigkeit_r = geschwindigkeit_r_values.mean()
    mean_geschwindigkeit_m = geschwindigkeit_m_values.mean()

    header = np.append(header, [versuch_name + '_mean_delta_l', versuch_name + '_mean_delta_r', versuch_name + '_mean_delta_m', versuch_name + '_mean_geschwindigkeit_l', versuch_name + '_mean_geschwindigkeit_r', versuch_name + '_mean_geschwindigkeit_m'])

    # Maxima bestimmen
    max_delta_l = delta_l_values.max()
    max_delta_r = delta_r_values.max()
    max_delta_m = delta_m_values.max()
    max_geschwindigkeit_l = geschwindigkeit_l_values.max()
    max_geschwindigkeit_r = geschwindigkeit_r_values.max()
    max_geschwindigkeit_m = geschwindigkeit_m_values.max()

    header = np.append(header, [versuch_name + '_max_delta_l', versuch_name + '_max_delta_r', versuch_name + '_max_delta_m', versuch_name + '_max_geschwindigkeit_l', versuch_name + '_max_geschwindigkeit_r', versuch_name + '_max_geschwindigkeit_m'])

    # Minima bestimmen
    min_delta_l = np.min(delta_l_values[np.nonzero(delta_l_values)])
    min_delta_r = np.min(delta_r_values[np.nonzero(delta_r_values)])
    min_delta_m = np.min(delta_m_values[np.nonzero(delta_m_values)])
    #Exceptionhandling fuer die Versuchspersonen, bei denen nur ein Auge gemessen wurde
    try:
        min_geschwindigkeit_l = np.min(geschwindigkeit_l_values[np.nonzero(geschwindigkeit_l_values)])
    except ValueError:
        min_geschwindigkeit_l = 0
    try:
        min_geschwindigkeit_r = np.min(geschwindigkeit_r_values[np.nonzero(geschwindigkeit_r_values)])
    except ValueError:
        min_geschwindigkeit_r = 0
    try:
        min_geschwindigkeit_m = np.min(geschwindigkeit_m_values[np.nonzero(geschwindigkeit_m_values)])
    except ValueError:
        min_geschwindigkeit_m = 0

    header = np.append(header, [versuch_name + '_min_delta_l', versuch_name + '_min_delta_r', versuch_name + '_min_delta_m', versuch_name + '_min_geschwindigkeit_l', versuch_name + '_min_geschwindigkeit_r', versuch_name + '_min_geschwindigkeit_m'])

    # Standardabweichungen berechnen
    std_delta_l = delta_l_values.std()
    std_delta_r = delta_r_values.std()
    std_delta_m = delta_m_values.std()
    std_geschwindigkeit_l = geschwindigkeit_l_values.std()
    std_geschwindigkeit_r = geschwindigkeit_r_values.std()
    std_geschwindigkeit_m = geschwindigkeit_m_values.std()

    header = np.append(header, [versuch_name + '_standardabweichung_delta_l', versuch_name + '_standardabweichung_delta_r', versuch_name + '_standardabweichung_delta_m', versuch_name + '_standardabweichung_geschwindigkeit_l', versuch_name + '_standardabweichung_geschwindigkeit_r', versuch_name + '_standardabweichung_geschwindigkeit_m'])
    
    # Varianzen berechnen
    var_delta_l = delta_l_values.var()
    var_delta_r = delta_r_values.var()
    var_delta_m = delta_m_values.var()
    var_geschwindigkeit_l = geschwindigkeit_l_values.var()
    var_geschwindigkeit_r = geschwindigkeit_r_values.var()
    var_geschwindigkeit_m = geschwindigkeit_m_values.var()

    header = np.append(header, [versuch_name + '_varianz_delta_l', versuch_name + '_varianz_delta_r', versuch_name + '_varianz_delta_m', versuch_name + '_varianz_geschwindigkeit_l', versuch_name + '_varianz_geschwindigkeit_r', versuch_name + '_varianz_geschwindigkeit_m'])

    # Tendenz auswerten
    condition_voraus_l = np.equal(tendenz_l_values,1)
    num_voraus_l = len(np.extract(condition_voraus_l, tendenz_l_values))
    condition_voraus_r = np.equal(tendenz_r_values,1)
    num_voraus_r = len(np.extract(condition_voraus_r, tendenz_r_values))
    condition_voraus_m = np.equal(tendenz_m_values,1)
    num_voraus_m = len(np.extract(condition_voraus_m, tendenz_m_values))
    condition_hinter_l = np.equal(tendenz_l_values,-1)
    num_hinter_l = len(np.extract(condition_hinter_l, tendenz_l_values))
    condition_hinter_r = np.equal(tendenz_r_values,-1)
    num_hinter_r = len(np.extract(condition_hinter_r, tendenz_r_values))
    condition_hinter_m = np.equal(tendenz_m_values,-1)
    num_hinter_m = len(np.extract(condition_hinter_m, tendenz_m_values))

    if num_voraus_l > num_hinter_l:
        tendenz_l = 1
    else:
        if num_hinter_l > num_voraus_l:
            tendenz_l = -1
        else:
            tendenz_l = 0
    if num_voraus_r > num_hinter_r:
            tendenz_r = 1
    else:
        if num_hinter_r > num_voraus_r:
            tendenz_r = -1
        else:
            tendenz_r = 0
    if num_voraus_m > num_hinter_m:
            tendenz_m = 1
    else:
        if num_hinter_m > num_voraus_m:
            tendenz_m = -1
        else:
            tendenz_m = 0

    header = np.append(header, [versuch_name + '_tendenz_l', versuch_name + '_tendenz_r', versuch_name + '_tendenz_m'])

    yield [[mean_delta_l, mean_delta_r, mean_delta_m, mean_geschwindigkeit_l, mean_geschwindigkeit_r, mean_geschwindigkeit_m, max_delta_l, max_delta_r, max_delta_m, max_geschwindigkeit_l, max_geschwindigkeit_r, max_geschwindigkeit_m, min_delta_l, min_delta_r, min_delta_m, min_geschwindigkeit_l, min_geschwindigkeit_r, min_geschwindigkeit_m, std_delta_l, std_delta_r, std_delta_m, std_geschwindigkeit_l, std_geschwindigkeit_r, std_geschwindigkeit_m, var_delta_l, var_delta_r, var_delta_m, var_geschwindigkeit_l, var_geschwindigkeit_r, var_geschwindigkeit_m, tendenz_l, tendenz_r, tendenz_m]]
    yield header 

def make_result_file():
    header_source =['t_tracker','pix_x','pix_y','zeitstempel','blick_l_x','blick_l_y','blick_r_x','blick_r_y','blick_m_x','blick_m_y','pix_x_translation','pix_y_translation','delta_l_t','delta_m_t','delta_r_t','geschwindigkeit_l','geschwindigkeit_m','geschwindigkeit_r','richtung_delta_l_x','richtung_delta_l_y','richtung_delta_m_x','richtung_delta_m_y','richtung_delta_r_x','richtung_delta_r_y', 'tendenz_l', 'tendenz_r', 'tendenz_m']
    header_destination = ['person']
    source_folders = os.listdir(cfg.extendedHome)
    
    # Ordner fuer das Ergebnis erstellen
    if os.path.exists(cfg.resultHome) == False:
        os.makedirs(cfg.resultHome)
    result = pd.DataFrame()

    source_path_h = os.path.join(cfg.extendedHome, 'horizontal') # horizontal
    source_path_l8 = os.path.join(cfg.extendedHome, 'liegende_acht_langsam') # langsame 8
    source_path_s8 = os.path.join(cfg.extendedHome, 'liegende_acht_schnell') # schnelle 8

    source_file_list = os.listdir(source_path_h)

    for source_file in source_file_list:
        #Die Dateien mit den Informationen zu der Anzahl werden ignoriert. Allerdings werden sie in dem else-Zweig trotzdem geoeffnet.
        if 'stats' in source_file:
            pass
        else:
            source_h = pd.read_csv(os.path.join(source_path_h, source_file), sep=',', names = header_source).ix[1:] # horizontal
            source_l8 = pd.read_csv(os.path.join(source_path_l8, source_file), sep=',', names = header_source).ix[1:] # langsame 8
            source_s8 = pd.read_csv(os.path.join(source_path_s8, source_file), sep=',', names = header_source).ix[1:] # schnelle 8
            
            # Horizontal
            werte = [[source_file[:-4]]]
            neu, header = versuch_auswerten(source_h, 'Horizontal', header_destination)
            werte = np.append(werte, neu)

            # langsame 8
            neu, header = versuch_auswerten(source_h, 'Liegende_8_langsam', header)
            werte = np.append(werte, neu)
            
            # schnelle 8
            neu, header = versuch_auswerten(source_h, 'Liegende_8_schnell', header)
            werte = np.append(werte, neu)
            
            df = pd.DataFrame([werte], columns=header)
            result = result.append(df)

    result.to_csv(os.path.join(cfg.resultHome, "result.csv"), index=False)
make_result_file()
