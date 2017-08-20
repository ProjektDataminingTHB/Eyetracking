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
    blick_l_x_values = pd.to_numeric(versuch_werte.blick_l_x).values
    blick_l_y_values = pd.to_numeric(versuch_werte.blick_l_y).values
    blick_r_x_values = pd.to_numeric(versuch_werte.blick_r_x).values
    blick_r_y_values = pd.to_numeric(versuch_werte.blick_r_y).values
    sacc_m_values = pd.to_numeric(versuch_werte.sacc_m).values
    sacc_l_values = pd.to_numeric(versuch_werte.sacc_l).values
    sacc_r_values = pd.to_numeric(versuch_werte.sacc_r).values

    # Mittelkwerte bestimmen
    # Kein Exceptionhandling, da ein leeres Array dazu fuehrt, dass np.mean() nan zurueckgibt und keine Exception
    if delta_l_values[np.nonzero(delta_l_values)].size == 0:
        mean_delta_l = -1
    else:
        mean_delta_l = np.mean(delta_l_values[np.nonzero(delta_l_values)])
    if delta_r_values[np.nonzero(delta_r_values)].size == 0:
        mean_delta_r = -1
    else:
        mean_delta_r = np.mean(delta_r_values[np.nonzero(delta_r_values)])
    if delta_m_values[np.nonzero(delta_m_values)].size == 0:
        mean_delta_m = -1
    else:
        mean_delta_m = np.mean(delta_m_values[np.nonzero(delta_m_values)])
    if geschwindigkeit_l_values[np.nonzero(geschwindigkeit_l_values)].size == 0:
        mean_geschwindigkeit_l = -1
    else:
        mean_geschwindigkeit_l = np.mean(geschwindigkeit_l_values[np.nonzero(geschwindigkeit_l_values)])
    if geschwindigkeit_r_values[np.nonzero(geschwindigkeit_r_values)].size == 0:
        mean_geschwindigkeit_r = -1
    else:
        mean_geschwindigkeit_r = np.mean(geschwindigkeit_r_values[np.nonzero(geschwindigkeit_r_values)])
    if geschwindigkeit_m_values[np.nonzero(geschwindigkeit_m_values)].size == 0:
        mean_geschwindigkeit_m = -1
    else:
        mean_geschwindigkeit_m = np.mean(geschwindigkeit_m_values[np.nonzero(geschwindigkeit_m_values)])

    header = np.append(header, [versuch_name + '_mean_delta_l', versuch_name + '_mean_delta_r', versuch_name + '_mean_delta_m', versuch_name + '_mean_geschwindigkeit_l', versuch_name + '_mean_geschwindigkeit_r', versuch_name + '_mean_geschwindigkeit_m'])

    # Maxima bestimmen
    try:
        max_delta_l = np.max(delta_l_values[np.nonzero(delta_l_values)])
    except ValueError:
        max_delta_l = -1
    try:
        max_delta_r = np.max(delta_r_values[np.nonzero(delta_r_values)])
    except ValueError:
        max_delta_r = -1
    try:
        max_delta_m = np.max(delta_m_values[np.nonzero(delta_m_values)])
    except ValueError:
        max_delta_m = -1
    try:
        max_geschwindigkeit_l = np.max(geschwindigkeit_l_values[np.nonzero(geschwindigkeit_l_values)])
    except ValueError:
        max_geschwindigkeit_l = -1
    try:
        max_geschwindigkeit_r = np.max(geschwindigkeit_r_values[np.nonzero(geschwindigkeit_r_values)])
    except ValueError:
        max_geschwindigkeit_r = -1
    try:
        max_geschwindigkeit_m = np.max(geschwindigkeit_m_values[np.nonzero(geschwindigkeit_m_values)])
    except ValueError:
        max_geschwindigkeit_m = -1

    header = np.append(header, [versuch_name + '_max_delta_l', versuch_name + '_max_delta_r', versuch_name + '_max_delta_m', versuch_name + '_max_geschwindigkeit_l', versuch_name + '_max_geschwindigkeit_r', versuch_name + '_max_geschwindigkeit_m'])

    # Minima bestimmen
    #Exceptionhandling fuer die Versuchspersonen, bei denen nur ein Auge gemessen wurde
    try:
        min_delta_l = np.min(delta_l_values[np.nonzero(delta_l_values)])
    except ValueError:
        min_delta_l = -1
    try:
        min_delta_r = np.min(delta_r_values[np.nonzero(delta_r_values)])
    except ValueError:
        min_delta_r = -1
    try:
        min_delta_m = np.min(delta_m_values[np.nonzero(delta_m_values)])
    except ValueError:
        min_delta_m = -1
    try:
        min_geschwindigkeit_l = np.min(geschwindigkeit_l_values[np.nonzero(geschwindigkeit_l_values)])
    except ValueError:
        min_geschwindigkeit_l = -1
    try:
        min_geschwindigkeit_r = np.min(geschwindigkeit_r_values[np.nonzero(geschwindigkeit_r_values)])
    except ValueError:
        min_geschwindigkeit_r = -1
    try:
        min_geschwindigkeit_m = np.min(geschwindigkeit_m_values[np.nonzero(geschwindigkeit_m_values)])
    except ValueError:
        min_geschwindigkeit_m = -1

    header = np.append(header, [versuch_name + '_min_delta_l', versuch_name + '_min_delta_r', versuch_name + '_min_delta_m', versuch_name + '_min_geschwindigkeit_l', versuch_name + '_min_geschwindigkeit_r', versuch_name + '_min_geschwindigkeit_m'])

    # Standardabweichungen berechnen
    if delta_l_values[np.nonzero(delta_l_values)].size == 0:
        std_delta_l = -1
    else:
        std_delta_l = np.std(delta_l_values[np.nonzero(delta_l_values)])
    if delta_r_values[np.nonzero(delta_r_values)].size == 0:
        std_delta_r = -1
    else:
        std_delta_r = np.std(delta_r_values[np.nonzero(delta_r_values)])
    if delta_m_values[np.nonzero(delta_m_values)].size == 0:
        std_delta_m = -1
    else:
        std_delta_m = np.std(delta_m_values[np.nonzero(delta_m_values)])
    if geschwindigkeit_l_values[np.nonzero(geschwindigkeit_l_values)].size == 0:
        std_geschwindigkeit_l = -1
    else:
        std_geschwindigkeit_l = np.std(geschwindigkeit_l_values[np.nonzero(geschwindigkeit_l_values)])
    if geschwindigkeit_r_values[np.nonzero(geschwindigkeit_r_values)].size == 0:
        std_geschwindigkeit_r = -1
    else:
        std_geschwindigkeit_r = np.std(geschwindigkeit_r_values[np.nonzero(geschwindigkeit_r_values)])
    if geschwindigkeit_m_values[np.nonzero(geschwindigkeit_m_values)].size == 0:
        std_geschwindigkeit_m = -1
    else:
        std_geschwindigkeit_m = np.std(geschwindigkeit_m_values[np.nonzero(geschwindigkeit_m_values)])

    header = np.append(header, [versuch_name + '_standardabweichung_delta_l', versuch_name + '_standardabweichung_delta_r', versuch_name + '_standardabweichung_delta_m', versuch_name + '_standardabweichung_geschwindigkeit_l', versuch_name + '_standardabweichung_geschwindigkeit_r', versuch_name + '_standardabweichung_geschwindigkeit_m'])
    
    # Varianzen berechnen
    if delta_l_values[np.nonzero(delta_l_values)].size == 0:
        var_delta_l = -1
    else:
        var_delta_l = np.var(delta_l_values[np.nonzero(delta_l_values)])
    if delta_r_values[np.nonzero(delta_r_values)].size == 0:
        var_delta_r = -1
    else:
        var_delta_r = np.var(delta_r_values[np.nonzero(delta_r_values)])
    if delta_m_values[np.nonzero(delta_m_values)].size == 0:
        var_delta_m = -1
    else:
        var_delta_m = np.var(delta_m_values[np.nonzero(delta_m_values)])
    if geschwindigkeit_l_values[np.nonzero(geschwindigkeit_l_values)].size == 0:
        var_geschwindigkeit_l = -1
    else:
        var_geschwindigkeit_l = np.var(geschwindigkeit_l_values[np.nonzero(geschwindigkeit_l_values)])
    if geschwindigkeit_r_values[np.nonzero(geschwindigkeit_r_values)].size == 0:
        var_geschwindigkeit_r = -1
    else:
        var_geschwindigkeit_r = np.var(geschwindigkeit_r_values[np.nonzero(geschwindigkeit_r_values)])
    if geschwindigkeit_m_values[np.nonzero(geschwindigkeit_m_values)].size == 0:
        var_geschwindigkeit_m = -1
    else:
        var_geschwindigkeit_m = np.var(geschwindigkeit_m_values[np.nonzero(geschwindigkeit_m_values)])

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

    # -100 steht fuer keinen errechneten Wert, sondern fuer nich vorhanden.
    if num_voraus_l == 0 and num_hinter_l == 0:
        tendenz_l = -100
    else:
        if num_voraus_l > num_hinter_l:
            tendenz_l = 1
        else:
            if num_hinter_l > num_voraus_l:
                tendenz_l = -1
            else:
                tendenz_l = 0
    
    if num_voraus_r == 0 and num_hinter_r == 0:
        tendenz_r = -100
    else:
        if num_voraus_r > num_hinter_r:
                tendenz_r = 1
        else:
            if num_hinter_r > num_voraus_r:
                tendenz_r = -1
            else:
                tendenz_r = 0

    if num_voraus_m == 0 and num_hinter_m == 0:
        tendenz_m = -100
    else:
        if num_voraus_m > num_hinter_m:
                tendenz_m = 1
        else:
            if num_hinter_m > num_voraus_m:
                tendenz_m = -1
            else:
                tendenz_m = 0

    header = np.append(header, [versuch_name + '_tendenz_l', versuch_name + '_tendenz_r', versuch_name + '_tendenz_m'])

    # Berechnung der Kovarianz vom linken und rechten Auge
    cov_x = np.cov(blick_l_x_values, blick_r_x_values)[0][1]
    cov_y = np.cov(blick_l_y_values, blick_r_y_values)[0][1]

    header = np.append(header, [versuch_name + '_Kovarianz_blick_x', versuch_name + '_Kovarianz_blick_y'])
    
    verhaeltnis_l_x_da = blick_l_x_values[np.nonzero(blick_l_x_values)].size / blick_l_x_values.size
    verhaeltnis_l_y_da = blick_l_y_values[np.nonzero(blick_l_y_values)].size / blick_l_y_values.size
    verhaeltnis_r_x_da = blick_r_x_values[np.nonzero(blick_r_x_values)].size / blick_r_x_values.size
    verhaeltnis_r_y_da = blick_r_y_values[np.nonzero(blick_r_y_values)].size / blick_r_y_values.size

    sacc_m = np.sum(sacc_m_values)
    sacc_l = np.sum(sacc_l_values)
    sacc_r = np.sum(sacc_r_values)
    if versuch_name == 'Horizontal' or versuch_name == 'Liegende_8_schnell':
        sacc_rate_m = sacc_m / (999*4)
        sacc_rate_l = sacc_l / (999*4)
        sacc_rate_r = sacc_r / (999*4)
    else:
        sacc_rate_m = sacc_m / (999*5)
        sacc_rate_l = sacc_l / (999*5)
        sacc_rate_r = sacc_r / (999*5)
    
    header = np.append(header, [versuch_name + '_links_verhaeltnis_x', versuch_name + '_links_verhaeltnis_y', versuch_name + '_rechts_verhaeltnis_x', versuch_name + '_rechts_verhaeltnis_y', versuch_name + '_sacc_m', versuch_name + '_sacc_rate_m', versuch_name + '_sacc_l', versuch_name + '_sacc_rate_l', versuch_name + '_sacc_r', versuch_name + '_sacc_rate_r'])

    yield [[mean_delta_l, mean_delta_r, mean_delta_m, mean_geschwindigkeit_l, mean_geschwindigkeit_r, mean_geschwindigkeit_m, max_delta_l, max_delta_r, max_delta_m, max_geschwindigkeit_l, max_geschwindigkeit_r, max_geschwindigkeit_m, min_delta_l, min_delta_r, min_delta_m, min_geschwindigkeit_l, min_geschwindigkeit_r, min_geschwindigkeit_m, std_delta_l, std_delta_r, std_delta_m, std_geschwindigkeit_l, std_geschwindigkeit_r, std_geschwindigkeit_m, var_delta_l, var_delta_r, var_delta_m, var_geschwindigkeit_l, var_geschwindigkeit_r, var_geschwindigkeit_m, tendenz_l, tendenz_r, tendenz_m, cov_x, cov_y, verhaeltnis_l_x_da, verhaeltnis_l_y_da, verhaeltnis_r_x_da, verhaeltnis_r_y_da, sacc_m, sacc_l, sacc_r, sacc_rate_m, sacc_rate_l, sacc_rate_r]]
    yield header 

def make_result_file():
    header_source =['t_tracker','pix_x','pix_y','zeitstempel','blick_l_x','blick_l_y','blick_r_x','blick_r_y','blick_m_x','blick_m_y','pix_x_translation','pix_y_translation','delta_l_t','delta_m_t','delta_r_t','geschwindigkeit_l','geschwindigkeit_m','geschwindigkeit_r', 'sacc_l', 'sacc_m', 'sacc_r','richtung_delta_l_x','richtung_delta_l_y','richtung_delta_m_x','richtung_delta_m_y','richtung_delta_r_x','richtung_delta_r_y', 'tendenz_l', 'tendenz_m', 'tendenz_r']
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
        #Die Dateien mit den Informationen zu der Anzahl werden ignoriert. Diese koennen genutzt werden, um ein detaillierteres Ergebnis zu erhalten.
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
            neu, header = versuch_auswerten(source_l8, 'Liegende_8_langsam', header)
            werte = np.append(werte, neu)
            
            # schnelle 8
            neu, header = versuch_auswerten(source_s8, 'Liegende_8_schnell', header)
            werte = np.append(werte, neu)
            
            df = pd.DataFrame([werte], columns=header)
            result = result.append(df)
    #
    # df2 = pd.DataFrame({'sacc_horizontal_l': np.array(h)[:, 0], 'sacc_horizontal_r': np.array(h)[:, 1], 'sacc_horizontal_m': np.array(h)[:, 2],
    #                     'sacc_rate_horizontal_l': (np.array(h)[:, 0])/(999*4), 'sacc_rate_horizontal_r': (np.array(h)[:, 1])/(999*4), 'sacc_rate_horizontal_m': (np.array(h)[:, 2])/(999*4),
    #                                    'sacc_langsam_l': np.array(l)[:, 0], 'sacc_langsam_r': np.array(l)[:, 1], 'sacc_langsam_m': np.array(l)[:, 2],
    #                                    'sacc_rate_langsam_l': (np.array(l)[:, 0])/(999*5), 'sacc_rate_langsam_r': (np.array(l)[:, 1])/(999*5), 'sacc_rate_langsam_m': (np.array(l)[:, 2])/(999*5),
    #                                    'sacc_schnell_l': np.array(s)[:, 0], 'sacc_schnell_r': np.array(s)[:, 1], 'sacc_schnell_m': np.array(s)[:, 2],
    #                                    'sacc_rate_schnell_l': (np.array(s)[:, 0])/(999*4), 'sacc_rate_schnell_r': (np.array(s)[:, 1])/(999*4), 'sacc_rate_schnell_m': (np.array(s)[:, 2])/(999*4)})
    # new_header = list(result)
    # new_header = new_header + list(df2)
    # values = np.concatenate((result.values, df2.values), axis=1)
    # r = pd.DataFrame(values, columns=header)
    result.to_csv(os.path.join(cfg.resultHome, "result.csv"), index=False)

# def saccade(input_blick = cfg.datenZerlegungHome):
#     threshold = berechne_threshold()
#     vps = os.listdir(input_blick)
#     horizontal = list()
#     liegende_acht_langsam = list()
#     liegende_acht_schnell = list()
#     m = 0
#     for vp in vps:
#         tmp = tls.remove_begin('vp_', vp)
#         tmp = tls.remove_begin('_stats', tmp)
#         n = int(tmp)
#         if n > m:
#             m = n
#
#     for i in range(m):
#         if not tls.int_to_str(i+1) in cfg.exclude:
#
#             root_path = os.path.join(input_blick, 'vp_{}'.format(tls.int_to_str(i+1)))
#             horizontal_path = os.path.join(root_path, 'horizontal')
#             langsam_path = os.path.join(root_path, 'liegende_acht_langsam')
#             schnell_path = os.path.join(root_path, 'liegende_acht_schnell')
#
#             h = os.walk(horizontal_path)
#             saccade_l = 0
#             saccade_r = 0
#             saccade_m = 0
#             for root, folders, files in h:
#                 #print(root, folders, files)
#                 if(len(folders) == 0):
#                     file = os.path.join(root, files[files.index('vp_{}_gaze.csv'.format(tls.int_to_str(i+1)))])
#                     df = pd.read_csv(file, sep=cfg.sep)
#                     vals = df.values[:, 1:]
#                     links = vals[:, :2]
#                     recht = vals[:, 2:]
#                     middle = (links + recht) / 2
#                     #print(get_saccades_fixations(links, threshold))
#                     saccade_l += get_saccades_fixations(links, threshold)[1]
#                     saccade_r += get_saccades_fixations(recht, threshold)[1]
#                     saccade_m += get_saccades_fixations(middle, threshold)[1]
#             tmp = list()
#             tmp.append(saccade_l)
#             tmp.append(saccade_r)
#             tmp.append(saccade_m)
#             horizontal.append(tmp)
#
#             s = os.walk(schnell_path)
#             saccade_l = 0
#             saccade_r = 0
#             saccade_m = 0
#             for root, folders, files in s:
#                 if(len(folders) == 0):
#                     file = os.path.join(root, files[files.index('vp_{}_gaze.csv'.format(tls.int_to_str(i+1)))])
#                     df = pd.read_csv(file, sep=cfg.sep)
#                     vals = df.values[:, 1:]
#                     links = vals[:, :2]
#                     recht = vals[:, 2:]
#                     middle = (links + recht ) / 2
#                     saccade_l += get_saccades_fixations(links, threshold)[1]
#                     saccade_r += get_saccades_fixations(recht, threshold)[1]
#                     saccade_m += get_saccades_fixations(middle, threshold)[1]
#             tmp = list()
#             tmp.append(saccade_l)
#             tmp.append(saccade_r)
#             tmp.append(saccade_m)
#             liegende_acht_schnell.append(tmp)
#
#             l = os.walk(langsam_path)
#             saccade_l = 0
#             saccade_r = 0
#             saccade_m = 0
#             for root, folders, files in l:
#                 if(len(folders) == 0):
#                     file = os.path.join(root, files[files.index('vp_{}_gaze.csv'.format(tls.int_to_str(i+1)))])
#                     df = pd.read_csv(file, sep=cfg.sep)
#                     vals = df.values[:, 1:]
#                     links = vals[:, :2]
#                     recht = vals[:, 2:]
#                     middle = (links + recht ) / 2
#                     saccade_l += get_saccades_fixations(links, threshold)[1]
#                     saccade_r += get_saccades_fixations(recht, threshold)[1]
#                     saccade_m += get_saccades_fixations(middle, threshold)[1]
#             tmp = list()
#             tmp.append(saccade_l)
#             tmp.append(saccade_r)
#             tmp.append(saccade_m)
#             liegende_acht_langsam.append(tmp)


    # final = list()
    # final.append(horizontal)
    # final.append(liegende_acht_langsam)
    # final.append(liegende_acht_schnell)
    # return horizontal, liegende_acht_langsam, liegende_acht_schnell

# def saccades():
#     horizontal = os.walk(cfg.horizontalHome)
#     for root, folders, files in horizontal:
#
#     pass

# def berechne_threshold():
#     f = os.walk(cfg.datenZerlegungHome)
#     threshold = 0
#     i = 0
#     for root, folders, files in f:
#         if folders == []:
#             file = os.path.join(root, 'target.csv')
#             df = pd.read_csv(file, sep=cfg.sep)
#             t_data = df.values[:, 1:]
#             th = get_eye_data_axis(t_data)
#             threshold = threshold + min(th[1:])
#             i += 1
#
#     return threshold / i

tls.showInfo('Beginn', 'Ausgangsdaten')
make_result_file()
tls.showInfo('Ende', 'Ausgangsdaten')
