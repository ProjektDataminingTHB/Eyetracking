import numpy as np
import pandas as pd
import os
import platform
from config import Config as cfg

def occurIn(exclude, str_name):
    for exc in exclude:
        if exc in str_name:
            return True
    return False

def remove_begin(pattern, string):
    l_pattern = len(pattern)
    l_string = len(string)
    if pattern in string:
        n_string = ''
        for i in range(l_pattern, l_string):
            n_string += string[i]
        return n_string
    else:
        return string

def remove_end(pattern, string):
    l_pattern = len(pattern)
    l_string = len(string)
    if pattern in string:
        n_string = ''
        for i in range(l_string - l_pattern):
            n_string += string[i]
        return n_string
    else:
        return string

def find_separator(seps, file):
    for sep in seps:
        inhalt_datei = pd.read_csv(file, sep=sep,
                                   names=['t_Tracker', 't_soll', 't_ist', 'pix_x', 'pix_y', 'deg_x',
                                          'deg_y'])
        for sep1 in seps:
            if sep1 != sep:
                if sep1 in inhalt_datei['t_Tracker'][1]:
                    return sep1
    return ''

def occur(e, list):
    i = 0
    for el in list:
        if el == e:
            i += 1
    return i

def index_messung(punkt, column, messung_number):
    column_tmp = list()

    for e in column:
        column_tmp.append(e)
    i = 0

    if 'Cycle:' not in punkt:
        while i < messung_number:
            column_tmp.remove(punkt)
            i += 1
    return column_tmp.index(punkt)

def gaze_zerlegung(begin, end, cycle_start, cycle_stop, erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte,
                   fuenfte_spalte, messung_number = 0):

    start = index_messung(begin, zweite_spalte, messung_number) + 1
    stop = index_messung(end, zweite_spalte, messung_number) + 1

    blick_l_x = zweite_spalte[start:stop]
    blick_l_y = dritte_spalte[start:stop]
    zeitstempel = erste_spalte[start:stop]
    blick_r_x = vierte_spalte[start:stop]
    blick_r_y = fuenfte_spalte[start:stop]

    index_start = index_messung(cycle_start, blick_l_x, messung_number) + 1
    index_stop = index_messung(cycle_stop, blick_l_x, messung_number)
    tmp = blick_l_x[index_start:index_stop]

    blick_l_y = blick_l_y[index_start:index_stop]
    zeitstempel = zeitstempel[index_start:index_stop]
    blick_r_x = blick_r_x[index_start:index_stop]
    blick_r_y = blick_r_y[index_start:index_stop]
    blick_l_x = tmp

    data1 = np.array([zeitstempel]).T
    data2 = np.array([blick_l_x]).T
    data5 = np.array([blick_l_y]).T
    data3 = np.array([blick_r_x]).T
    data4 = np.array([blick_r_y]).T

    data = np.concatenate((data1, data2, data5, data3, data4), axis=1)
    return data

def struktur_erstellung(begin, end, cycle_start, cycle_stop, messung, cycle, messung_number, erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte, experiment,
                                        header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name):

    data = gaze_zerlegung(begin, end, cycle_start, cycle_stop, erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte, messung_number = messung_number)
    ordner = ausgabe_ordner + '/' + ausgabe_prefix + csv_name
    if os.path.exists(ordner) == False:
        os.mkdir(ordner)

    ordner = ordner + '/' + experiment
    if os.path.exists(ordner) == False:
        os.mkdir(ordner)

    ordner = ordner + '/' + messung
    if os.path.exists(ordner) == False:
        os.mkdir(ordner)

    ordner = ordner + '/' + cycle
    if os.path.exists(ordner) == False:
        os.mkdir(ordner)

    df = pd.DataFrame(data, columns = header)
    df.to_csv(ordner + '/' + ausgabe_prefix + csv_name + ausgabe_blick_suffix + '.csv', index=False)

def zerlegung(ausgabe_ordner = cfg.datenZerlegungHome, eingabe_ordner = cfg.rawDataHome,
												eingabe_prefix = 'vp_', eingabe_blick_suffix = '_gaze', ausgabe_prefix = 'vp_', ausgabe_blick_suffix = '_gaze',
												messung_ordner_prefix = 'messung', probe_ordner_prefix = 'probe', delim = ' '):
    err_ordner_not_exist = 'Der Ordner {} ist nicht vorhanden'
    header = ['zeitstempel', 'blick_l_x', 'blick_l_y', 'blick_r_x', 'blick_r_y']
    header_target = ['t_tracker', 'pix_x', 'pix_y']
    experimente = ['liegende_acht_langsam', 'liegende_acht_schnell', 'horizontal']
    seps = [';', ' ', ',']
    messungen = ['messung1', 'messung2', 'probe']
    cycles = ['cycle1', 'cycle2']

    if os.path.exists(eingabe_ordner) == False:
        print(err_ordner_not_exist.format(eingabe_ordner))
        return

    if os.path.exists(ausgabe_ordner) == False:
        os.mkdir(ausgabe_ordner)

    csv_dateien = os.listdir(eingabe_ordner)

    i = 1
    print('{}% abgeschlossen'.format(0))
    for csv_datei in csv_dateien:
        if('linux' in platform.system().lower()):
            os.system('clear')
        if ('windows' in platform.system().lower()):
            os.system('cls')
        print('{}% abgeschlossen'.format(int(i * 100 / len(csv_dateien))))
        if csv_datei.lower().endswith('.txt'):
            csv_name = csv_datei.split('.')[0]
            csv_name = remove_begin(eingabe_prefix, csv_name)
            if not occurIn(cfg.exclude, csv_name):
                if eingabe_blick_suffix in csv_name:    #Kontroll, ob sich die Datei mit gaze endet
                    csv_name = remove_end(eingabe_blick_suffix, csv_name)
                    inhalt_datei = pd.read_csv(eingabe_ordner + '/' + csv_datei, sep = delim, names=['zeitstempel', 'blick_l_x', 'blick_l_y',
                                                                                                     'pupillen_grosse_l', 'pos_l_x', 'pos_l_y',
                                                                                                     'pos_entf_l', 'blick_r_x', 'blick_r_y',
                                                                                                     'pupillen_grosse_r', 'pos_r_x', 'pos_r_y',
                                                                                                     'pos_entf_r'])
                    erste_spalte = list(inhalt_datei['zeitstempel'])
                    zweite_spalte = list(inhalt_datei['blick_l_x'])
                    dritte_spalte = list(inhalt_datei['blick_l_y'])
                    vierte_spalte = list(inhalt_datei['blick_r_x'])
                    fuenfte_spalte = list(inhalt_datei['blick_r_y'])

                    #Beschränkung des Dateimatrix
                    struktur_erstellung('PURSUIT:Cycles=1:Trajectory=lying_eight:T=8', 'PURSUIT_FINISHED:Cycles=1:Trajectory=lying_eight:T=8',
                                          'Cycle:1:START', 'Cycle:1:STOP', messungen[2], cycles[0], 0, erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                            experimente[0], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)
                    struktur_erstellung('PURSUIT:Cycles=2:Trajectory=lying_eight:T=8', 'PURSUIT_FINISHED:Cycles=2:Trajectory=lying_eight:T=8',
                                          'Cycle:1:START', 'Cycle:1:STOP', messungen[0], cycles[0], 0, erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                            experimente[0], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)
                    struktur_erstellung('PURSUIT:Cycles=2:Trajectory=lying_eight:T=8', 'PURSUIT_FINISHED:Cycles=2:Trajectory=lying_eight:T=8',
                                          'Cycle:2:START', 'Cycle:2:STOP', messungen[0], cycles[1], 0, erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                            experimente[0], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)
                    struktur_erstellung('PURSUIT:Cycles=2:Trajectory=lying_eight:T=8', 'PURSUIT_FINISHED:Cycles=2:Trajectory=lying_eight:T=8',
                                          'Cycle:1:START', 'Cycle:1:STOP', messungen[1], cycles[0], 1, erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                            experimente[0], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)
                    struktur_erstellung('PURSUIT:Cycles=2:Trajectory=lying_eight:T=8', 'PURSUIT_FINISHED:Cycles=2:Trajectory=lying_eight:T=8',
                                          'Cycle:2:START', 'Cycle:2:STOP', messungen[1], cycles[1], 1, erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                            experimente[0], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)

                    struktur_erstellung('PURSUIT:Cycles=2:Trajectory=lying_eight:T=4', 'PURSUIT_FINISHED:Cycles=2:Trajectory=lying_eight:T=4',
                                          'Cycle:1:START', 'Cycle:1:STOP', messungen[0], cycles[0], 0, erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                            experimente[1], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)
                    struktur_erstellung('PURSUIT:Cycles=2:Trajectory=lying_eight:T=4', 'PURSUIT_FINISHED:Cycles=2:Trajectory=lying_eight:T=4',
                                          'Cycle:2:START', 'Cycle:2:STOP', messungen[0], cycles[1], 0, erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                            experimente[1], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)
                    struktur_erstellung('PURSUIT:Cycles=2:Trajectory=lying_eight:T=4', 'PURSUIT_FINISHED:Cycles=2:Trajectory=lying_eight:T=4',
                                          'Cycle:1:START', 'Cycle:1:STOP', messungen[1], cycles[0], 1, erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                            experimente[1], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)
                    struktur_erstellung('PURSUIT:Cycles=2:Trajectory=lying_eight:T=4', 'PURSUIT_FINISHED:Cycles=2:Trajectory=lying_eight:T=4',
                                          'Cycle:2:START', 'Cycle:2:STOP', messungen[1], cycles[1], 1, erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                            experimente[1], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)

                    struktur_erstellung('PURSUIT:Cycles=2:Trajectory=line_linear:T=4', 'PURSUIT_FINISHED:Cycles=2:Trajectory=line_linear:T=4',
                                          'Cycle:1:START', 'Cycle:1:STOP', messungen[0], cycles[0], 0, erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                            experimente[2], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)
                    struktur_erstellung('PURSUIT:Cycles=2:Trajectory=line_linear:T=4', 'PURSUIT_FINISHED:Cycles=2:Trajectory=line_linear:T=4',
                                          'Cycle:2:START', 'Cycle:2:STOP', messungen[0], cycles[1], 0, erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                            experimente[2], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)
                    struktur_erstellung('PURSUIT:Cycles=2:Trajectory=line_linear:T=4', 'PURSUIT_FINISHED:Cycles=2:Trajectory=line_linear:T=4',
                                          'Cycle:1:START', 'Cycle:1:STOP', messungen[1], cycles[0], 1, erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                            experimente[2], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)
                    struktur_erstellung('PURSUIT:Cycles=2:Trajectory=line_linear:T=4', 'PURSUIT_FINISHED:Cycles=2:Trajectory=line_linear:T=4',
                                          'Cycle:2:START', 'Cycle:2:STOP', messungen[1], cycles[1], 1, erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                            experimente[2], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)

                else:
                    file = eingabe_ordner + '/' + csv_datei
                    sep = find_separator(seps, file)
                    inhalt_datei = pd.read_csv(eingabe_ordner + '/' + csv_datei, sep = sep, names=['t_Tracker', 't_soll', 't_ist', 'pix_x', 'pix_y', 'deg_x', 'deg_y'])

                    data1 = list(inhalt_datei['t_Tracker'])
                    data2 = list(inhalt_datei['pix_x'])
                    data3 = list(inhalt_datei['pix_y'])

                    data1 = data1[1:]
                    data2 = data2[1:]
                    data3 = data3[1:]

                    data = np.concatenate((np.array([data1]).T,
                                          np.array([data2]).T,
                                            np.array([data3]).T), axis = 1)
                    ordner = ausgabe_ordner + '/' + ausgabe_prefix + csv_name
                    if os.path.exists(ordner) == False:
                        os.mkdir(ordner)

                    df = pd.DataFrame(data, columns=header_target)
                    df.to_csv(ordner + '/' + ausgabe_prefix + csv_name + '.csv', index=False)
        i += 1
    print('Komplete Zerlegung abgeschlossen !!!')
default_input = cfg.rawDataHome
default_output = cfg.datenZerlegungHome

input_path = input('Wo ist Ihr Datenordner ({})?_ '.format(default_input))
output_path = input('Wo würden Sie die Zerlegung ablegen ({})?_ '.format(default_output))

if input_path == '':
    input_path = default_input

if output_path == '':
    output_path = default_output

zerlegung(eingabe_ordner = input_path, ausgabe_ordner = output_path)