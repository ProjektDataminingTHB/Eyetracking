import pandas as pd
import numpy as np
import os
from config import Config as cfg
import tools as tls
import ntpath

def zuordnung_matched():
    header_target = ['t_tracker', 'pix_x', 'pix_y']
    header_blick = ['zeitstempel', 'blick_l_x', 'blick_l_y',
                                                'blick_r_x', 'blick_r_y']

    #nimmt eine Liste von Listen, die alle Ordner und Unterordner in einer Liste von Länge 3 darstellen Wurzel, alle Ordner, alle dateien darstellen.
    all_folders = os.walk(cfg.datenZerlegungHome)
    for root, folders, files in all_folders:
        #überprüft, ob wir in dem Ordner einer Versuchsperson (mit 3 oexperimenten und eine Targetdatei) in Daten_zerlegung sind
        if len(folders) == 3 and len(files) == 1:
            for exp in folders:
                #Wenn ja, wird für jedes Expereriment ein Ordner festgelegt
                if os.path.exists(os.path.join(cfg.matchedHome, exp)) == False:
                    os.makedirs(os.path.join(cfg.matchedHome, exp))

                #Ordner zur Erstellung des Matching wird festgelegt
                output_folder = os.path.join(cfg.matchedHome, exp)

                all_folders_2 = os.walk(os.path.join(root, exp))
                data = np.zeros((1, len(header_target) + len(header_blick)))
                stats = list()
                header_stats = list()
                for root_2, folders_2, files_2 in all_folders_2:
                    if len(folders_2) == 0 and len(files_2) == 2:
                        parent, cycle = ntpath.split(root_2)
                        parent, messung = ntpath.split(parent)
                        files_2.sort()
                        target = pd.read_csv(os.path.join(root_2, files_2[0]), sep=',',
                                             names=header_target)
                        blick = pd.read_csv(os.path.join(root_2, files_2[1]), sep=',',
                                                names=header_blick)
                        target_array = target.values[1:, :]
                        blick_array = blick.values[1:, :]
                        j = 0
                        count = 0

                        for i in np.arange(np.size(target_array, 0)):
                            while j < np.size(blick_array, 0) and blick_array[j, 0] < target_array[i, 0]:
                                j += 1
                            matched_row = np.concatenate((target_array[i, :], blick_array[j, :]), axis = 0)
                            data = np.concatenate((data,
                                                np.array([matched_row])), axis=0)
                            count += 1
                        header_stats.append(messung + '_' + cycle)
                        stats.append(count)

                data = data[1:, :]
                df = pd.DataFrame(data, columns=['t_tracker', 'pix_x', 'pix_y', 'zeitstempel', 'blick_l_x', 'blick_l_y',
                                               'blick_r_x', 'blick_r_y'])
                filename = tls.remove_end('_gaze.csv', files_2[1])
                stats = np.array([stats])
                stats_file = pd.DataFrame(stats, columns = header_stats)
                df.to_csv(os.path.join(output_folder, filename + '.csv'), index=False)
                stats_file.to_csv(os.path.join(output_folder, filename + '_stats' + '.csv'), index=False)

zuordnung_matched()