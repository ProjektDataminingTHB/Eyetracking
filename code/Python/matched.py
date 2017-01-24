import pandas as pd
import numpy as np
import os
from config import Config as cfg
import tools as tls

def zuordnung_matched():
    all_folders = os.walk(cfg.datenZerlegungHome)
    for root, folders, files in all_folders:
        if len(folders) == 3 and len(files) == 1:
            for exp in folders:
                if os.path.exists(os.path.join(cfg.matchedHome, exp)) == False:
                    os.makedirs(os.path.join(cfg.matchedHome, exp))

                output_folder = os.path.join(cfg.matchedHome, exp)

                all_folders_2 = os.walk(os.path.join(root, exp))
                for root_2, folders_2, files_2 in all_folders_2:
                    if len(folders_2) == 0 and len(files_2) == 2:
                        files_2.sort()
                        target = pd.read_csv(os.path.join(root_2, files_2[0]), sep=',',
                                             names=['t_tracker', 'pix_x', 'pix_y'])
                        blick = pd.read_csv(os.path.join(root_2, files_2[1]), sep=',',
                                                names=['zeitstempel', 'blick_l_x', 'blick_l_y',
                                                'blick_r_x', 'blick_r_y'])
                        target_array = target.values[1:, :]
                        blick_array = blick.values[1:, :]
                        j = 0
                        already_assign = False
                        for i in np.arange(np.size(target_array, 0)):
                            while j < np.size(blick_array, 0) and blick_array[j, 0] < target_array[i, 0]:
                                j += 1
                            matched_row = np.concatenate((target_array[i, :], blick_array[j, :]), axis = 0)
                            if not already_assign:
                                zero = np.zeros((1, matched_row.size))
                                data = zero + matched_row.astype(float)
                                already_assign = True
                            else:
                                data = np.concatenate((data,
                                                    np.array([matched_row])), axis=0)

                df = pd.DataFrame(data, columns=['t_tracker', 'pix_x', 'pix_y', 'zeitstempel', 'blick_l_x', 'blick_l_y',
                                                'blick_r_x', 'blick_r_y'])
                filename = tls.remove_end('_gaze.csv', files_2[1])
                df.to_csv(os.path.join(output_folder, filename + '.csv'), index=False)

zuordnung_matched()