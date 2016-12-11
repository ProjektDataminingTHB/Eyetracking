import numpy as np
import pandas as pd
import os
import shutil
import platform

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

def gaze_zerlegung(begin, end, cycle_start, cycle_stop, erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte,
                   fuenfte_spalte):
        blick_l_x = zweite_spalte[
                    zweite_spalte.index(begin) + 1:zweite_spalte.index(
                        end)]
        blick_l_y = dritte_spalte[
                    zweite_spalte.index(begin) + 1:zweite_spalte.index(
                        end)]
        zeitstempel = erste_spalte[
                      zweite_spalte.index(begin) + 1:zweite_spalte.index(
                          end)]
        blick_r_x = vierte_spalte[
                    zweite_spalte.index(begin) + 1:zweite_spalte.index(
                        end)]
        blick_r_y = fuenfte_spalte[
                    zweite_spalte.index(begin) + 1:zweite_spalte.index(
                        end)]
        try:
            tmp = blick_l_x[blick_l_x.index(cycle_start) + 1:blick_l_x.index(cycle_end)]
            blick_l_y = blick_l_y[blick_l_x.index(cycle_start) + 1:blick_l_x.index(cycle_end)]
            zeitstempel = zeitstempel[blick_l_x.index(cycle_start) + 1:blick_l_x.index(cycle_end)]
            blick_r_x = blick_r_x[blick_l_x.index(cycle_start) + 1:blick_l_x.index(cycle_end)]
            blick_r_y = blick_r_y[blick_l_x.index(cycle_start) + 1:blick_l_x.index(cycle_end)]
            blick_l_x = tmp
        except:
            try:
                tmp = blick_l_x[blick_l_x.index(cycle_start) + 1:blick_l_x.index(
                    end)]
                blick_l_y = blick_l_y[blick_l_x.index(cycle_start) + 1:blick_l_x.index(
                    end)]
                zeitstempel = zeitstempel[blick_l_x.index(cycle_start) + 1:blick_l_x.index(
                    end)]
                blick_r_x = blick_r_x[blick_l_x.index(cycle_start) + 1:blick_l_x.index(
                    end)]
                blick_r_y = blick_r_y[blick_l_x.index(cycle_start) + 1:blick_l_x.index(
                    end)]
                blick_l_x = tmp
            except:
                try:
                    tmp = blick_l_x[blick_l_x.index(
                        begin) + 1:blick_l_x.index(cycle_end)]
                    blick_l_y = blick_l_y[
                                blick_l_x.index(begin) + 1:blick_l_x.index(
                                    cycle_end)]
                    zeitstempel = zeitstempel[
                                  blick_l_x.index(begin) + 1:blick_l_x.index(
                                      cycle_end)]
                    blick_r_x = blick_r_x[
                                blick_l_x.index(begin) + 1:blick_l_x.index(
                                    cycle_end)]
                    blick_r_y = blick_r_y[
                                blick_l_x.index(begin) + 1:blick_l_x.index(
                                    cycle_end)]
                    blick_l_x = tmp
                except:
                    pass  # das heißt, wir haben schon die richtige menge

        data1 = np.array([zeitstempel]).T
        data2 = np.array([blick_l_x]).T
        data3 = np.array([blick_r_x]).T
        data4 = np.array([blick_r_y]).T
        data5 = np.array([blick_l_y]).T

        data = np.concatenate((data1, data2, data3, data4, data5), axis=1)
        return data

def struktur_erstellung(begin, end, cycle_start, cycle_stop, messung, erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte, experiment,
                                        header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name):

    data = gaze_zerlegung(begin, end, cycle_start, cycle_stop, erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte)
    ordner = ausgabe_ordner + '/' + ausgabe_prefix + csv_name
    if os.path.exists(ordner) == False:
        os.mkdir(ordner)

    ordner = ordner + '/' + experiment
    if os.path.exists(ordner) == False:
        os.mkdir(ordner)

    ordner = ordner + '/' + messung
    if os.path.exists(ordner) == False:
        os.mkdir(ordner)

    df = pd.DataFrame(data, columns = header)
    df.to_csv(ordner + '/' + ausgabe_prefix + csv_name + ausgabe_blick_suffix + '.csv', index=False)

def zerlegung(ausgabe_ordner = './daten_zerlegung', eingabe_ordner = './', eingabe_prefix = 'vp_', eingabe_blick_suffix = '_gaze', ausgabe_prefix = 'vp_', ausgabe_blick_suffix = '_gaze', messung_ordner_prefix = 'messung', probe_ordner_prefix = 'probe', delim = ' '):
    err_ordner_not_exist = 'Der Ordner {} ist nicht vorhanden'
    header = ['zeitstempel', 'blick_l_x', 'blick_l_y', 'blick_r_x', 'blick_r_y']
    experimente = ['liegende_acht_langsam', 'liegende_acht_schnell', 'horizontal']
    messungen = ['messung_1', 'messung_2', 'probe']

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
            if eingabe_blick_suffix in csv_name:
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

                struktur_erstellung('PURSUIT:Cycles=1:Trajectory=lying_eight:T=8', 'PURSUIT_FINISHED:Cycles=1:Trajectory=lying_eight:T=8',
                                      'Cycle:1:START', 'Cycle:1:STOP', messungen[2], erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                        experimente[0], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)
                struktur_erstellung('PURSUIT:Cycles=2:Trajectory=lying_eight:T=8', 'PURSUIT_FINISHED:Cycles=2:Trajectory=lying_eight:T=8',
                                      'Cycle:1:START', 'Cycle:1:STOP', messungen[0], erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                        experimente[0], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)
                struktur_erstellung('PURSUIT:Cycles=2:Trajectory=lying_eight:T=8', 'PURSUIT_FINISHED:Cycles=2:Trajectory=lying_eight:T=8',
                                      'Cycle:2:START', 'Cycle:2:STOP', messungen[0], erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                        experimente[0], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)
                struktur_erstellung('PURSUIT:Cycles=2:Trajectory=lying_eight:T=8', 'PURSUIT_FINISHED:Cycles=2:Trajectory=lying_eight:T=8',
                                      'Cycle:1:START', 'Cycle:1:STOP', messungen[1], erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                        experimente[0], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)
                struktur_erstellung('PURSUIT:Cycles=2:Trajectory=lying_eight:T=8', 'PURSUIT_FINISHED:Cycles=2:Trajectory=lying_eight:T=8',
                                      'Cycle:2:START', 'Cycle:2:STOP', messungen[1], erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                        experimente[0], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)

                struktur_erstellung('PURSUIT:Cycles=2:Trajectory=lying_eight:T=4', 'PURSUIT_FINISHED:Cycles=2:Trajectory=lying_eight:T=4',
                                      'Cycle:1:START', 'Cycle:1:STOP', messungen[0], erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                        experimente[1], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)
                struktur_erstellung('PURSUIT:Cycles=2:Trajectory=lying_eight:T=4', 'PURSUIT_FINISHED:Cycles=2:Trajectory=lying_eight:T=4',
                                      'Cycle:2:START', 'Cycle:2:STOP', messungen[0], erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                        experimente[1], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)
                struktur_erstellung('PURSUIT:Cycles=2:Trajectory=lying_eight:T=4', 'PURSUIT_FINISHED:Cycles=2:Trajectory=lying_eight:T=4',
                                      'Cycle:1:START', 'Cycle:1:STOP', messungen[1], erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                        experimente[1], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)
                struktur_erstellung('PURSUIT:Cycles=2:Trajectory=lying_eight:T=4', 'PURSUIT_FINISHED:Cycles=2:Trajectory=lying_eight:T=4',
                                      'Cycle:2:START', 'Cycle:2:STOP', messungen[1], erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                        experimente[1], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)

                struktur_erstellung('PURSUIT:Cycles=2:Trajectory=line_linear:T=4', 'PURSUIT_FINISHED:Cycles=2:Trajectory=line_linear:T=4',
                                      'Cycle:1:START', 'Cycle:1:STOP', messungen[0], erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                        experimente[2], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)
                struktur_erstellung('PURSUIT:Cycles=2:Trajectory=line_linear:T=4', 'PURSUIT_FINISHED:Cycles=2:Trajectory=line_linear:T=4',
                                      'Cycle:2:START', 'Cycle:2:STOP', messungen[0], erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                        experimente[2], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)
                struktur_erstellung('PURSUIT:Cycles=2:Trajectory=line_linear:T=4', 'PURSUIT_FINISHED:Cycles=2:Trajectory=line_linear:T=4',
                                      'Cycle:1:START', 'Cycle:1:STOP', messungen[1], erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                        experimente[2], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)
                struktur_erstellung('PURSUIT:Cycles=2:Trajectory=line_linear:T=4', 'PURSUIT_FINISHED:Cycles=2:Trajectory=line_linear:T=4',
                                      'Cycle:2:START', 'Cycle:2:STOP', messungen[1], erste_spalte, zweite_spalte, dritte_spalte, vierte_spalte, fuenfte_spalte,
                                        experimente[2], header, ausgabe_ordner, ausgabe_prefix, ausgabe_blick_suffix, csv_name)

            else:
                ordner = ausgabe_ordner + '/' + ausgabe_prefix + csv_name
                if os.path.exists(ordner) == False:
                    os.mkdir(ordner)
                shutil.copy(eingabe_ordner + '/' + csv_datei, ordner)
        i += 1
    print('Komplete Zerlegung abgeschlossen !!!')
default_input = './daten'
default_output = './daten_zerlegung'

input_path = input('Wo ist Ihr Datenordner ({})?_ '.format(default_input))
output_path = input('Wo würden Sie die Zerlegung ablegen ({})?_ '.format(default_output))

if input_path == '':
    input_path = default_input

if output_path == '':
    output_path = default_output

zerlegung(eingabe_ordner = input_path, ausgabe_ordner = output_path)