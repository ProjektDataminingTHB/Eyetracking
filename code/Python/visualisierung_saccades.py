import matplotlib.pylab as plt
import numpy as np
from config import Config as cfg
import tools as tls
import os
import math
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn import preprocessing

vp = 77

def plots(input_blick = os.path.join(cfg.datenZerlegungHome, 'vp_{}/liegende_acht_schnell/messung2/cycle2/vp_{}_gaze.csv'.format(tls.int_to_str(vp), tls.int_to_str(vp))),
          input_target = os.path.join(cfg.datenZerlegungHome, 'vp_{}/liegende_acht_schnell/messung2/cycle2/target.csv'.format(tls.int_to_str(vp))),
          output_path = './', vp = vp, exp = 'liegende_acht_langsam', messung = 'messung2', cycle = 'cycle2', delim = ','):

    title = 'Versuchperson {}, {}, {}, {}'.format(tls.int_to_str(vp), exp, messung, cycle)
    data = np.genfromtxt(
            input_blick,
            delimiter=delim)
    target_data = np.genfromtxt(
            input_target,
            delimiter = delim)

    data_array = np.array(data[1:, :])
    target_data_array = np.array(target_data[1:, :])
    target_data_array = target_data_array[:, 1:]

    time_axis = get_time_axis(data_array[:, 0])
    # link = data_array[:, 1:3]
    recht = data_array[:, 3:]
    # link_axis = get_eye_data_axis(link)
    recht_axis = get_eye_data_axis(recht)
    r = get_saccades_fixations(time_axis[1:], recht, target_data_array)
    print(r)

    # plt.plot(time_axis, link_axis, 'b', label='Blick., l. Auge')
    plt.plot(time_axis, recht_axis, 'g', label='Distanzen der Blickpunkte., r. Auge')
    plt.plot(np.array([0, np.max(time_axis)]), np.array([r[2], r[2]]), 'r', label='Threshold = {}'.format(r[2]))
    # plt.axis([0, time_axis[np.size(time_axis) - 1], 0, (max(np.max(link_axis), np.max(link_axis)) + min(np.mean(link_axis[1:]), np.mean(link_axis[1:])))*4])
    plt.title(title)
    plt.ylabel('Distanz')
    plt.xlabel('Zeit (ms)')
    plt.legend(loc='upper right', shadow=True, fontsize=9, ncol=4, mode="expand")
    # plt.savefig(os.path.join(cfg.finalHome, title + '.pdf'))
    plt.show()
    plt.close()

def get_time_axis(time):
    time_axis = np.zeros_like(time)
    for i in range(np.size(time) - 1):
        time_axis[i + 1] = time_axis[i] + (time[i + 1] - time[i])/1000

    return time_axis

def get_eye_data_axis(data):
    data_distance = np.zeros((np.size(data, axis=0), 1))
    for i in range(np.size(data, axis=0) - 1):
        data_distance[i + 1] = math.sqrt((data[i + 1, 0] - data[i, 0])**2 + (data[i + 1, 1] - data[i, 1])**2)/4

    return data_distance

def get_saccades_fixations(x, Y, T):

    r = list()
    recht_axis = get_eye_data_axis(Y)
    target_axis = get_eye_data_axis(T)
    threshold = min(target_axis[1:])
    r.append(np.sum(recht_axis < threshold))
    r.append(np.sum(recht_axis > threshold))
    r.append(threshold)
    return r

plots()