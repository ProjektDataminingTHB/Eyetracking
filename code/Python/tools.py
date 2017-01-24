from random import randint
import pandas as pd
import platform
import os
from config import Config as cfg


def list_str_to_int(l):
    ll = list()
    for e in l:
        ll.append(int(e))
    return ll

def int_to_str(val, digit = 3):
    char = str(val)
    if len(char) >= digit:
        return char
    else:
        if len(char) < digit:
            j = digit - len(char)
            for i in range(j):
                char = '0' + char
            return char

def random_choice(elements):
    ind = randint(0, len(elements) - 1)
    return elements[ind]

def percentage(n, N):
    if ('linux' in platform.system().lower()):
        os.system('clear')
    if ('windows' in platform.system().lower()):
        os.system('cls')
    print('{}% abgeschlossen'.format(int(n * 100 / N)))

def count_file(input_dir = cfg.datenZerlegungHome, ext = '', exp = ''):
    d = os.walk(input_dir)
    n = 0
    for sd in d:
        if len(sd[1]) == 0:
            files = os.listdir(sd[0])
            for file in files:
                if ext != '' and exp != '':
                    if file.lower().endswith('.' + ext) and exp.lower() in file.lower():
                        n += 1
                if ext != '' and exp == '':
                    if file.lower().endswith('.' + ext):
                        n += 1
                if ext == '' and exp != '':
                    if exp.lower() in file.lower():
                        n += 1
                else:
                    n += 1
    return n

def vp_min_max(images):
    if images != []:
        vp_name = images[0].split('-')[0]
        vp_number = int(vp_name.split('_')[1])
        vp_min = vp_number
        vp_max = vp_number
        for image in images:
            vp_name = image.split('-')[0]
            vp_number = int(vp_name.split('_')[1])
            if vp_number < vp_min:
                vp_min = vp_number
            if vp_number > vp_max:
                vp_max = vp_number
        return vp_min, vp_max
    else:
        return 0, 0


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

def finde_ersten_wert(zeitstempelliste, suchwert):
    for anfang in zeitstempelliste:
        try:
            differenz = suchwert - anfang
            if differenz < 0:
                return anfang
        except:
            pass


def finde_letzten_wert(zeitstempelliste, suchwert, anfang):
    ende = 0
    zeitstempelliste1 = list(zeitstempelliste[zeitstempelliste.index(anfang):])
    for ende1 in zeitstempelliste1:
        try:
            differenz = suchwert - ende1
            if differenz < 0:
                return ende
            else:
                # in dem Fall möchten wir den Wert, vor dem Wert, der die Bedingung erfüllt haben
                ende = ende1
        except:
            pass