import matplotlib.pylab as plt
import numpy as np
import platform
from random import randint
import os
from config import Config as cfg

experimente = ['liegende_acht_langsam', 'liegende_acht_schnell', 'horizontal']
messungen = ['messung1', 'messung2', 'probe']
cycles = ['cycle1', 'cycle2']

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

def plots(input_blick = cfg.datenZerlegungHome + 'vp_045/liegende_acht_schnell/messung2/cycle2/vp_045_gaze.csv',
          input_target = cfg.datenZerlegungHome + 'vp_045/liegende_acht_schnell/messung2/vp_045.csv',
          output_path = './', vp = 45, exp = 'liegende_acht_langsam', messung = 'messung2', cycle = 'cycle2', delim = ','):


    head, tail = os.path.split(input_target)
    filename = tail.split('.')[0]

    data = np.genfromtxt(
            input_blick,
            delimiter = delim)
    target_data = np.genfromtxt(
            input_target,
            delimiter = delim)

    data_array = np.array(data[1:, :])
    target_data_array = np.array(target_data[1:, :])

    target_zeit = target_data_array[:, 0]
    target_data_array = target_data_array[:, 1:]

    zeit = data_array[:, 0]
    link = data_array[:, 1:3]
    recht = data_array[:, 3:]

    mitte = np.array([(link[:, 0] + recht[:, 0]) / 2, (link[:, 1] + recht[:, 1]) / 2])
    mitte = mitte.T

    target_mitte = np.array([np.mean(target_data_array[:, 0]), np.mean(target_data_array[:, 1])])
    mitte_mitte = np.array([np.mean(mitte[:, 0]), np.mean(mitte[:, 1])])

    u = mitte_mitte - target_mitte

    z_target_data_array = target_data_array + u
    div_x = 10
    div_y = 10
    tresh_x = np.mean(mitte[:, 0])
    tresh_y = np.mean(mitte[:, 1])

    fig = plt.figure()
    plt.plot(target_data_array[:, 0], target_data_array[:, 1], 'r', marker='x', markersize = 8, label='Targetpunkte')
    plt.plot(z_target_data_array[:, 0], z_target_data_array[:, 1], 'r', marker='x', markersize = 8, label='Targetpunkte')
    plt.plot(target_mitte[0], target_mitte[1], 'y', marker='o', markersize = 11, label='Mitte der Targetpunkte')
    plt.plot(mitte_mitte[0], mitte_mitte[1], 'c', marker='o', markersize = 18, label='Mitte der Blickpunkte')
    plt.plot(link[:, 0], link[:, 1], 'b', marker='o', label='Blick., l. Auge')
    plt.plot(recht[:, 0], recht[:, 1], 'g', marker='^', label='Blickp., r. Auge')
    plt.axis([min(np.min(link[:, 0]), np.min(recht[:, 0]), np.min(target_data_array[:, 0])) - tresh_x / div_x,
              max(np.max(link[:, 0]), np.max(recht[:, 0]), np.max(target_data_array[:, 0])) + tresh_x / div_x,
              min(np.min(link[:, 1]), np.min(recht[:, 1]), np.min(target_data_array[:, 1])) - tresh_y / div_y,
              max(np.max(link[:, 1]), np.max(recht[:, 1]), np.max(target_data_array[:, 1])) + tresh_y / div_y])
    plt.legend(loc='lower right', shadow=True, )
    plt.title('Versuchperson {}, {}, {}, {}'.format(int_to_str(vp), exp, messung, cycle))
    plt.ylabel('y')
    plt.xlabel('x')

    #im_ani = animation.ArtistAnimation(fig, ims, interval=50, repeat_delay=3000,
    #                                   blit=True)
    plt.savefig(output_path + filename + '-{}-{}-{}.png'.format(exp, messung, cycle))
    plt.show()
    plt.close()

plots()