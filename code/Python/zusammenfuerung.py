from config import Config as cfg
import tools as tls
import os

all_folders = os.walk(cfg.datenZerlegungHome)
    for root, folders, files in all_folders: