import matplotlib.pylab as plt
import numpy as np
from config import Config as cfg
import tools as tls

vp = 68

def plots(input_blick = cfg.datenZerlegungHome + 'vp_{}/liegende_acht_schnell/messung2/cycle2/vp_{}_gaze.csv'.format(tls.int_to_str(vp), tls.int_to_str(vp)),
          input_target = cfg.datenZerlegungHome + 'vp_{}/liegende_acht_schnell/messung2/cycle2/target.csv'.format(tls.int_to_str(vp)),
          output_path = './', vp = vp, exp = 'liegende_acht_langsam', messung = 'messung2', cycle = 'cycle2', delim = ','):

    data = np.genfromtxt(
            input_blick,
            delimiter = delim)
    target_data = np.genfromtxt(
            input_target,
            delimiter = delim)

    data_array = np.array(data[1:, :])
    target_data_array = np.array(target_data[1:, :])

    target_data_array = target_data_array[:, 1:]

    link = data_array[:, 1:3]
    recht = data_array[:, 3:]

    mitte = np.array([(link[:, 0] + recht[:, 0]) / 2, (link[:, 1] + recht[:, 1]) / 2])
    mitte = mitte.T

    target_mitte = np.array([np.mean(target_data_array[:, 0]), np.mean(target_data_array[:, 1])])
    mitte_mitte = np.array([np.mean(mitte[:, 0]), np.mean(mitte[:, 1])])

    u = cfg.o_prim - cfg.o

    target_data_array[:, 1] = -1 * target_data_array[:, 1]
    z_target_data_array = target_data_array + u

    plt.plot(target_data_array[:, 0], target_data_array[:, 1], 'r', marker='x', markersize = 8, label='Targetpunkte')
    plt.plot(z_target_data_array[:, 0], z_target_data_array[:, 1], 'k', marker='*', markersize = 8, label='transformierte Targetpunkte')
    plt.plot(target_mitte[0], target_mitte[1], 'y', marker='o', markersize = 11, label='Mitte der Targetpunkte')
    plt.plot(mitte_mitte[0], mitte_mitte[1], 'c', marker='o', markersize = 18, label='Mitte der Blickpunkte')
    plt.plot(cfg.o_prim[0], cfg.o_prim[1], 'm', marker='+', markersize = 18, label='Ursprung')
    plt.plot(mitte[:, 0], mitte[:, 1], 'm', marker='o', label='Blick., Mitte')
    plt.plot(link[:, 0], link[:, 1], 'b', marker='o', label='Blick., l. Auge')
    plt.plot(recht[:, 0], recht[:, 1], 'g', marker='^', label='Blickp., r. Auge')
    plt.axis([-1*cfg.o_prim[0] + min(np.min(mitte[:, 0]), np.min(z_target_data_array[:, 0])),
                  cfg.o_prim[0] + max(np.max(mitte[:, 0]), np.max(z_target_data_array[:, 0])),
                  -1 * cfg.o_prim[1] +min(np.min(mitte[:, 1]), np.min(z_target_data_array[:, 1])),
                  cfg.o_prim[1] + max(np.max(mitte[:, 1]), np.max(z_target_data_array[:, 1]))])
    plt.legend(loc='lower right', shadow=True, )
    plt.title('Versuchperson {}, {}, {}, {}'.format(tls.int_to_str(vp), exp, messung, cycle))
    plt.ylabel('y')
    plt.xlabel('x')

    plt.show()
    plt.close()

plots()