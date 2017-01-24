import matplotlib.pylab as plt
import numpy as np
from config import Config as cfg
import tools as tls
import pandas as pd
import os

vp = 75
exp = 'liegende_acht_langsam'
experiment = os.path.join(cfg.matchedHome, exp)
stats = pd.read_csv(os.path.join(experiment, 'vp_{}_stats.csv'.format(tls.int_to_str(vp))), sep=',')
stats = stats.values

n_col = 3
n_lig = np.size(stats, 1) / n_col
diff = n_lig - int(n_lig)
if(diff != 0):
    n_lig = int(n_lig) + 1

plt.figure(1)
plt.subplot(n_lig, n_col, 1)

colors_target = ['r', 'k', 'm', 'c', 'b', 'g']
colors_blick = ['g', 'b', 'c', 'm', 'k', 'r']

def plots(input_target = os.path.join(experiment, 'vp_{}.csv'.format(tls.int_to_str(vp))), vp = vp, messung = 'messung2', cycle = 'cycle2'):

    data = np.genfromtxt(input_target, delimiter=',')
    data_array = np.array(data[1:, 4:])
    target_data_array = np.array(data[1:, 1:3])

    link = data_array[:, 0:2]
    recht = data_array[:, 2:]

    mitte = np.array([(link[:, 0] + recht[:, 0]) / 2, (link[:, 1] + recht[:, 1]) / 2])
    mitte = mitte.T

    u = cfg.o_prim - cfg.o

    target_data_array[:, 1] = -1 * target_data_array[:, 1]
    z_target_data_array = target_data_array + u
    for i in range(np.size(stats, 1)):
        start = 0
        if i != 0:
            start = np.sum(stats[0, :i])
            plt.subplot(n_lig, n_col, i + 1)
        plt.plot(target_data_array[start:start + stats[0, i], 0], target_data_array[start:start + stats[0, i], 1], 'r', marker='x', markersize = 8, label='Targetpunkte')
        plt.plot(z_target_data_array[start:start + stats[0, i], 0], z_target_data_array[start:start + stats[0, i], 1], 'k', marker='*', markersize = 8, label='transformierte Targetpunkte')
        plt.plot(mitte[start:start + stats[0, i], 0], mitte[start:start + stats[0, i], 1], 'm', marker='o', label='Blick., Mitte')
        plt.plot(link[start:start + stats[0, i], 0], link[start:start + stats[0, i], 1], 'b', marker='o', label='Blick., l. Auge')
        plt.plot(recht[start:start + stats[0, i], 0], recht[start:start + stats[0, i], 1], 'g', marker='^', label='Blickp., r. Auge')
        plt.axis([-1*cfg.o_prim[0] + min(np.min(mitte[:, 0]), np.min(z_target_data_array[:, 0])),
                      cfg.o_prim[0] + max(np.max(mitte[:, 0]), np.max(z_target_data_array[:, 0])),
                      -1 * cfg.o_prim[1] +min(np.min(mitte[:, 1]), np.min(z_target_data_array[:, 1])),
                      cfg.o_prim[1] + max(np.max(mitte[:, 1]), np.max(z_target_data_array[:, 1]))])

        plt.title('Versuchperson {}, {}, {}, {}'.format(tls.int_to_str(vp), exp, messung, cycle))
        plt.ylabel('y')
        plt.xlabel('x')

    plt.show()

plots()