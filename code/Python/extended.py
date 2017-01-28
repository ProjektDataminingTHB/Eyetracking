import pandas as pd
import numpy as np
import os
from config import Config as cfg
import tools as tls
import ntpath
from shutil import copyfile
import math

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
            if 'stats' in source_file:
                copyfile(os.path.join(source_path, source_file), os.path.join(destination_path, source_file))
            else:
                source = pd.read_csv(os.path.join(source_path, source_file), sep=',', names = header_source).ix[1:]
                middle_eyes = source.assign(blick_m_x = pd.to_numeric(source.blick_l_x) / 2 + pd.to_numeric(source.blick_r_x) / 2, blick_m_y = pd.to_numeric(source.blick_l_y) / 2 + pd.to_numeric(source.blick_r_y) / 2, pix_x_translation = pd.to_numeric(source.pix_x).add(640), pix_y_translation = (pd.to_numeric(source.pix_y) * -1).add(512))
                
                result = middle_eyes.assign(delta_l_t = lambda x : np.sqrt(np.power(pd.to_numeric(x.blick_l_x) - pd.to_numeric(x.pix_x_translation),2) + np.power(pd.to_numeric(x.blick_l_y) - pd.to_numeric(x.pix_y_translation),2)), delta_r_t = lambda x : np.sqrt(np.power(pd.to_numeric(x.blick_r_x) - pd.to_numeric(x.pix_x_translation),2) + np.power(pd.to_numeric(x.blick_r_y) - pd.to_numeric(x.pix_y_translation),2)), delta_m_t = lambda x : np.sqrt(np.power(pd.to_numeric(x.blick_m_x) - pd.to_numeric(x.pix_x_translation),2) + np.power(pd.to_numeric(x.blick_m_y) - pd.to_numeric(x.pix_y_translation),2)))

                result.to_csv(os.path.join(destination_path, source_file), index=False)

extend_files()
