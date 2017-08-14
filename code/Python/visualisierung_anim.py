import matplotlib.pylab as plt
import numpy as np
import matplotlib.animation as animation
from config import Config as cfg
import tools as tls
import os

vp = tls.int_to_str(300)

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

def animate(i):
    data = np.genfromtxt(os.path.join(cfg.datenZerlegungHome, 'vp_{}/liegende_acht_langsam/messung2/cycle2/vp_{}_gaze.csv'.format(vp, vp)),
        delimiter=',')
    target_data = np.genfromtxt(os.path.join(cfg.datenZerlegungHome, 'vp_{}/liegende_acht_langsam/messung2/cycle2/target.csv'.format(vp, vp)),
        delimiter=',')

    data_array = np.array(data[1:, :])
    target_data_array = np.array(target_data[1:, :])

    target_zeit = target_data_array[:, 0]
    target_data_array = target_data_array[:, 1:]

    u = cfg.o_prim - cfg.o

    target_data_array[:, 1] = -1 * target_data_array[:, 1]
    z_target_data_array = target_data_array + u

    zeit = data_array[:, 0]
    link = data_array[:, 1:3]
    recht = data_array[:, 3:]

    mitte = np.array([(link[:, 0] + recht[:, 0]) / 2, (link[:, 1] + recht[:, 1]) / 2])
    mitte = mitte.T


    k = int(np.size(zeit, 0) / np.size(target_zeit, 0))

    if i < np.size(mitte, 0):
        tls.percentage(i, np.size(mitte, 0))
        if i % k == 0:
            plt.plot(z_target_data_array[int(i / k), 0], z_target_data_array[int(i / k), 1], 'r', marker='x', markersize = 8, label='Targetpunkte')
        plt.plot(mitte[i, 0], mitte[i, 1], 'b', marker='o', label='Blickpunkte linkes Auge')
        plt.axis([-1*cfg.o_prim[0] + min(np.min(mitte[:, 0]), np.min(z_target_data_array[:, 0])),
                  cfg.o_prim[0] + max(np.max(mitte[:, 0]), np.max(z_target_data_array[:, 0])),
                  -1 * cfg.o_prim[1] +min(np.min(mitte[:, 1]), np.min(z_target_data_array[:, 1])),
                  cfg.o_prim[1] + max(np.max(mitte[:, 1]), np.max(z_target_data_array[:, 1]))])

ani = animation.FuncAnimation(fig, animate, interval = 0.0003)
print("Animation started")
plt.show()
print("Animation finished")