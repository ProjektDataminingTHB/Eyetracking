import matplotlib.pylab as plt
import numpy as np
import matplotlib.animation as animation
from config import Config as cfg
import tools as tls

vp = tls.int_to_str(70)

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

def animate(i):
    data = np.genfromtxt(cfg.datenZerlegungHome + 'vp_{}/liegende_acht_langsam/messung1/cycle2/vp_{}_gaze.csv'.format(vp, vp),
        delimiter=',')
    target_data = np.genfromtxt(cfg.datenZerlegungHome + 'vp_{}/liegende_acht_langsam/messung1/vp_{}.csv'.format(vp, vp),
        delimiter=',')

    data_array = np.array(data[1:, :])
    target_data_array = np.array(target_data[1:, :])

    target_zeit = target_data_array[:, 0]
    target_data_array = target_data_array[:, 1:]

    zeit = data_array[:, 0]
    link = data_array[:, 1:3]
    recht = data_array[:, 3:]

    mitte = np.array([(link[:, 0] + recht[:, 0]) / 2, (link[:, 1] + recht[:, 1]) / 2])
    mitte = mitte.T


    k = int(np.size(zeit, 0) / np.size(target_zeit, 0))

    div_x = 10
    div_y = 10
    tresh_x = np.mean(mitte[:, 0])
    tresh_y = np.mean(mitte[:, 1])

    if i < np.size(mitte, 0):
        tls.percentage(i, np.size(mitte, 0))
        if i % k == 0:
            plt.plot(target_data_array[int(i / k), 0], target_data_array[int(i / k), 1], 'r', marker='x', markersize = 8, label='Targetpunkte')
        plt.plot(mitte[i, 0], mitte[i, 1], 'b', marker='o', label='Blickpunkte')
        plt.axis([np.min(mitte[:, 0]) - tresh_x, np.max(mitte[:, 0]) + tresh_x / div_x, np.min(mitte[:, 1]) - tresh_y, np.max(mitte[:, 1]) + tresh_y / div_y])

ani = animation.FuncAnimation(fig, animate, interval = 0.00001)
print("Animation started")
plt.show()
print("Animation finished")