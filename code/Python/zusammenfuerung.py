from config import Config as cfg
import tools as tls
import os
import shutil

all_folders = os.walk(cfg.rawDataHome)
for root, folders, files in all_folders:
    max = -1
    for file in files:

        number = tls.get_number(file)

        if max < number:
            max = number

all_folders = os.walk(cfg.rawDataSoSe2017Home)
for root, folders, files in all_folders:
    sort_files = files.copy()
    sort_files.sort()

    for file in sort_files:
        number = tls.get_number(file)
        new_number = number + max
        str_number = tls.int_to_str(new_number)

        file_name = '{}{}'.format(cfg.prefix, str_number)
        if cfg.gaze in file:
            file_name += cfg.gaze
        file_name += '.txt'

        shutil.move(os.path.join(root,file), os.path.join(cfg.rawDataHome,file_name))