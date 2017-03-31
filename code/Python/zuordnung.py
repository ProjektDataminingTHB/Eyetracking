import pandas as pd
import numpy as np
import os
from config import Config as cfg
import tools as tls

def zuordnung():
    all_folders = os.walk(cfg.datenZerlegungHome)
    for root, folders, files in all_folders:
        if len(folders) == 3 and len(files) == 1:
            target = pd.read_csv(os.path.join(root, files[0]), sep=',', names=['t_tracker', 'pix_x', 'pix_y'])
            for exp in folders:
                all_folders_2 = os.walk(os.path.join(root, exp))
                for root_2, folders_2, files_2 in all_folders_2:
                    if len(folders_2) == 0:
                        blick = pd.read_csv(os.path.join(root_2, files_2[0]), sep=',', names=['zeitstempel', 'blick_l_x', 'blick_l_y',
                                                                                              'blick_r_x', 'blick_r_y'])
                        zt_blick = np.array(tls.list_str_to_int(list(blick['zeitstempel'][1:])))
                        zt_target = target['t_tracker'].values[1:]
                        target_array = target.values[1:, :]

                        zt_blick_min = np.min(zt_blick)
                        zt_blick_max = np.max(zt_blick)

                        row = 0
                        already_assign = False
                        for zt in zt_target:
                            if int(zt_blick_min) < int(zt) and int(zt_blick_max) > int(zt):
                                target_row = target_array[row, :]
                                if not already_assign:
                                    zero = np.zeros((1, target_row.size))
                                    data = zero + target_row.astype(float)
                                    already_assign = True
                                else:
                                    data = np.concatenate((data,
                                                       np.array([target_row])), axis=0)
                            row += 1
                        df = pd.DataFrame(data, columns=['t_tracker', 'pix_x', 'pix_y'])
                        df.to_csv(os.path.join(root_2, 'target.csv'), index=False)

tls.showInfo('Beginn', 'Datenzuordnung')
zuordnung()
tls.showInfo('Ende', 'Datenzuordnung')