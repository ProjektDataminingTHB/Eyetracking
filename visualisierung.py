import pandas as pd
import matplotlib.pylab as plt
import numpy as np
import matplotlib.animation as animation
import platform
import os


<<<<<<< HEAD
data = np.genfromtxt(
        '/home/herval/Documents/THB/Master/Semester1/Projekt1/DataMining/ProjektAufgabe/Eyetracking/daten_zerlegung/vp_001/liegende_acht_langsam/messung_2/cycle2/vp_001_gaze.csv',
        delimiter=',')
target_data = np.genfromtxt(
        '/home/herval/Documents/THB/Master/Semester1/Projekt1/DataMining/ProjektAufgabe/Eyetracking/daten_zerlegung/vp_001/liegende_acht_langsam/messung_2/vp_001.csv',
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
plt.plot(target_data_array[:, 0], target_data_array[:, 1], 'r', marker='x', markersize = 8, label='Targetpunkte')
plt.plot(link[:, 0], link[:, 1], 'b', marker='o', label='Blickpunkte')
plt.plot(recht[:, 0], recht[:, 1], 'g', marker='^', label='Blickpunkte')
plt.axis([np.min(mitte[:, 0]) - tresh_x, np.max(mitte[:, 0]) + tresh_x / div_x, np.min(mitte[:, 1]) - tresh_y, np.max(mitte[:, 1]) + tresh_y / div_y])
#plt.axis([np.min(link[:, 0]) - tresh_x, np.max(link[:, 0]) + tresh_x / div_x, np.min(link[:, 1]) - tresh_y, np.max(link[:, 1]) + tresh_y / div_y])
#plt.axis([np.min(recht[:, 0]) - tresh_x, np.max(recht[:, 0]) + tresh_x / div_x, np.min(recht[:, 1]) - tresh_y, np.max(recht[:, 1]) + tresh_y / div_y])


plt.show()
=======
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

def percentage(n, N):
    if ('linux' in platform.system().lower()):
        os.system('clear')
    if ('windows' in platform.system().lower()):
        os.system('cls')
    print('{}% abgeschlossen'.format(int(n * 100 / N)))


def animate(i):
    data = np.genfromtxt(
        './daten_zerlegung/vp_045/liegende_acht_langsam/messung_2/cycle2/vp_045_gaze.csv',
        delimiter=',')
    target_data = np.genfromtxt(
        './daten_zerlegung/vp_045/liegende_acht_langsam/messung_2/vp_045.csv',
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
        percentage(i, np.size(mitte, 0))
        if i % k == 0:
            plt.plot(target_data_array[int(i / k), 0], target_data_array[int(i / k), 1], 'r', marker='x', markersize = 8, label='Targetpunkte')
        plt.plot(mitte[i, 0], mitte[i, 1], 'b', marker='o', label='Blickpunkte')
        plt.axis([np.min(mitte[:, 0]) - tresh_x / div_x, np.max(mitte[:, 0]) + tresh_x / div_x, np.min(mitte[:, 1]) - tresh_y / div_y, np.max(mitte[:, 1]) + tresh_y / div_y])

ani = animation.FuncAnimation(fig, animate, interval = 1)
print("Animation started")
plt.show()
print("Animation finished")
>>>>>>> 69bcb79edbc994eaf40d683cdfd48bc89768a1cb
