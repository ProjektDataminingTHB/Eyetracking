import matplotlib.pylab as plt
import numpy as np
import matplotlib.animation as animation
from config import Config as cfg
import tools as tls
import pandas as pd
import os

exp = 'liegende_acht_langsam'
experiment = os.path.join(cfg.matchedHome, exp)
vp = tls.int_to_str(302)
stats = pd.read_csv(os.path.join(experiment, 'vp_{}_stats.csv'.format(vp)), sep=',')
header_stats = list(stats.columns.values)
print(header_stats)
stats = stats.values

n_col = 3
n_lig = np.size(stats, 1) / n_col

diff = n_lig - int(n_lig)
if(diff != 0):
    n_lig = int(n_lig) + 1

fig = plt.figure()
fig.add_subplot(n_lig, n_col, 1)

colors_target = ['r', 'k', 'm', 'c', 'b', 'g']
colors_blick = ['g', 'b', 'c', 'm', 'k', 'r']

data = np.genfromtxt(os.path.join(experiment, 'vp_{}.csv'.format(vp)), delimiter=',')
data_array = np.array(data[1:, 4:])
target_data_array = np.array(data[1:, 1:3])

u = cfg.o_prim - cfg.o

target_data_array[:, 1] = -1 * target_data_array[:, 1]
z_target_data_array = target_data_array + u

link = data_array[:, 0:2]
recht = data_array[:, 2:]

mitte = np.array([(link[:, 0] + recht[:, 0]) / 2, (link[:, 1] + recht[:, 1]) / 2])
mitte = mitte.T

k = int(np.size(data_array, 0) / np.size(target_data_array, 0))

def animate(i):
    global current_stat, j
    if i < np.size(mitte, 0):
        if i == 0:
            current_stat = 0
            j = 0
        if i - current_stat >= stats[0, j] and j < np.size(stats, 1):
            current_stat += stats[0, j]
            j += 1
            fig.add_subplot(n_lig, n_col, j + 1)
        #tls.percentage(i, np.size(mitte, 0))

        plt.title('Versuchperson {}, {}, {}'.format(vp, exp, header_stats[j]))
        if i % k == 0:
            plt.plot(z_target_data_array[int(i / k), 0], z_target_data_array[int(i / k), 1], colors_target[j], marker='x', markersize = 8, label='Targetpunkte')
        plt.plot(mitte[i, 0], mitte[i, 1], colors_blick[j], marker='o', label='Blickpunkte linkes Auge')
        plt.axis([-1*cfg.o_prim[0] + min(np.min(mitte[:, 0]), np.min(z_target_data_array[:, 0])),
                  cfg.o_prim[0] + max(np.max(mitte[:, 0]), np.max(z_target_data_array[:, 0])),
                  -1 * cfg.o_prim[1] +min(np.min(mitte[:, 1]), np.min(z_target_data_array[:, 1])),
                  cfg.o_prim[1] + max(np.max(mitte[:, 1]), np.max(z_target_data_array[:, 1]))])

ani = animation.FuncAnimation(fig, animate, interval = 0.0001)
print("Animation started")
plt.show()
print("Animation finished")