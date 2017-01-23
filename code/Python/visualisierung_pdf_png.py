import matplotlib.pylab as plt
import numpy as np
from random import randint
import os
from config import Config as cfg
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes
from reportlab.lib.utils import ImageReader
import tools as tls

experimente = ['liegende_acht_langsam', 'liegende_acht_schnell', 'horizontal']
messungen = ['messung1', 'messung2', 'probe']
cycles = ['cycle1', 'cycle2']

def plots(input_blick = cfg.datenZerlegungHome + 'vp_045/liegende_acht_langsam/messung2/cycle2/vp_045_gaze.csv',
          input_target = cfg.datenZerlegungHome + 'vp_045/liegende_acht_langsam/messung2/vp_045.csv',
          output_path = cfg.visualisierungBilderHome, vp = 1, exp = 'liegende_acht_langsam', messung = 'messung2', cycle = 'cycle2', delim = ','):


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


    div_x = 10
    div_y = 10
    tresh_x = np.mean(mitte[:, 0])
    tresh_y = np.mean(mitte[:, 1])

    fig = plt.figure()
    plt.plot(target_data_array[:, 0], target_data_array[:, 1], 'r', marker='x', markersize = 8, label='Targetpunkte')
    plt.plot(link[:, 0], link[:, 1], 'b', marker='o', label='Blick., l. Auge')
    plt.plot(recht[:, 0], recht[:, 1], 'g', marker='^', label='Blickp., r. Auge')
    plt.axis([min(np.min(link[:, 0]), np.min(recht[:, 0]), np.min(target_data_array[:, 0])) - tresh_x / div_x,
              max(np.max(link[:, 0]), np.max(recht[:, 0]), np.max(target_data_array[:, 0])) + tresh_x / div_x,
              min(np.min(link[:, 1]), np.min(recht[:, 1]), np.min(target_data_array[:, 1])) - tresh_y / div_y,
              max(np.max(link[:, 1]), np.max(recht[:, 1]), np.max(target_data_array[:, 1])) + tresh_y / div_y])
    plt.legend(loc='lower right', shadow=True, )
    plt.title('Versuchperson {}, {}, {}, {}'.format(vp, exp, messung, cycle))
    plt.ylabel('y')
    plt.xlabel('x')

    plt.savefig(output_path + filename + '-{}-{}-{}.png'.format(exp, messung, cycle))
    plt.close()
    #plt.show()


def gen_images(input_dir = cfg.datenZerlegungHome,
               output_dir = cfg.visualisierungBilderHome,
               n_images = 0, vp_list = [], vp_select = 1, acht = -1, messung = -1, cycle = -1):
    print('Generierung der Bilder in dem Ornder {}'.format(output_dir))
    print('Bitte, haben Sie ein bisschen Geduld !')
    if os.path.exists(input_dir) == False:
        print('Der Inputsordner ist nicht vorhanden')
    else:
        if os.path.exists(output_dir) == False:
            os.mkdir(output_dir)

        if n_images != len(vp_list) and vp_select == 0:
            print('Die Anzahl der zu generierenden Bilder und der eingegebenen Versuchspersonen stimmen nicht überein')
        else:
            if vp_select < 2:
                for i in range(n_images):
                    if acht == 0:
                        exp = experimente[0]
                    if acht == 1:
                        exp = experimente[1]
                    if acht == 2:
                        exp = experimente[2]

                    if messung == 1:
                        mess = messungen[0]
                    if messung == 2:
                        mess = messungen[1]

                    if cycle == 1:
                        cyc = cycles[0]
                    if cycle == 2:
                        cyc = cycles[1]

                    if acht < 0 or acht > 2:
                        exp = tls.random_choice(experimente)

                    if messung < 0 or messung > 2:
                        mess = tls.random_choice(messungen)
                        while mess == messungen[2] and (exp == experimente[1] or exp == experimente[2]):
                            mess = tls.random_choice(messungen)
                    if cycle < 0 or cycle > 2:
                        cyc = tls.random_choice(cycles)
                        if mess == messungen[2]:
                            cyc = cycles[0]
                    if vp_select == 1:
                        vp_num = tls.int_to_str(randint(1, 130))
                    else:
                        vp_num = tls.int_to_str(vp_list[i])

                    plots(input_blick = '{}vp_{}/{}/{}/{}/vp_{}_gaze.csv'.format(input_dir, vp_num, exp, mess, cyc, vp_num),
                                    input_target = '{}vp_{}/{}/{}/vp_{}.csv'.format(input_dir, vp_num, exp, mess, vp_num),
                                    output_path = output_dir, vp = vp_num, exp = exp, messung = mess, cycle = cyc,
                                    delim = ',')
            else:
                if vp_select == 2:
                    n_files = tls.count_file()
                    n_col = 2
                    n_lig = int(n_files / n_col)
                    n_lig += (n_files + n_lig)
                    d = os.walk(input_dir)
                    n = 1
                    for sd in d:
                        if sd[1] == []:
                            parent = sd[0].split('/')
                            parent = '/'.join(parent[0:len(parent) - 1])
                            files = os.listdir(parent + '/')

                            for file in files:
                                if file.endswith(".csv"):
                                    target = file
                            vp_num = target.split('_')[1]
                            exp = sd[0].split('/')[len(sd[0].split('/')) - 3]
                            mess = sd[0].split('/')[len(sd[0].split('/')) - 2]
                            cyc = sd[0].split('/')[len(sd[0].split('/')) - 1]
                            plots(input_blick = sd[0] + '/' + sd[2][0],
                                      input_target = parent + '/' + target,
                                      output_path=output_dir, vp=vp_num, exp=exp, messung=mess, cycle=cyc,
                                      delim=',')
                        n += 1
                        #plt.savefig(output_dir + 'bilder.png')
                        #pp = PdfPages('multipage.pdf')
                        #pp.savefig()
                else:
                    print('Der eingegebene vp_select-Wert ist falsch')

def gen_pdf_images(input_dir = cfg.visualisierungBilderHome,
            output_dir = cfg.visualisierungPdfHome,
            pdf_name = 'visualisierung'):

    print('\nGenerierung der PDF-dateien in dem Ornder {}'.format(output_dir))
    print('Bitte, haben Sie ein bisschen Geduld !')
    if os.path.exists(output_dir) == False:
        os.mkdir(output_dir)

    if os.path.exists(input_dir) == False:
        os.mkdir(input_dir)

    images = os.listdir(input_dir)
    for exp in experimente:
        pages = canvas.Canvas(output_dir + pdf_name + '_' + exp + '.pdf', pagesize=A4)
        pW, pH = pagesizes.A4
        n_col = 3
        n_lig = 8
        space = pW / 100
        iW = (pW - (space * n_col + 1))/ n_col
        iH = (pH - (space * n_lig + 1))/ n_lig
        col = 0
        lig = 0
        n_current_page = 1
        n_page = tls.count_file(input_dir, ext = 'png', exp = exp) / (n_col * n_lig)

        if exp == experimente[0]:
            n_page /= 5
        else:
            n_page /= 4

        if n_page != int(n_page):
            n_page = int(n_page) + 1
        n_page += 1

        vp_min, vp_max = tls.vp_min_max(images)
        for i in range(vp_min, vp_max + 1):
            for mess in messungen:
                if not(exp != experimente[0] and mess == messungen[2]):
                    for cyc in cycles:
                        image = 'vp_{}-{}-{}-{}.png'.format(tls.int_to_str(i), exp, mess, cyc)
                        if os.path.exists(input_dir + image) == True:
                            if exp in image:
                                if image.lower().endswith('.png'):
                                    if col == n_col:
                                        col = 0
                                        lig += 1
                                    if lig == n_lig:
                                        lig = 0
                                        #pages.drawString(pW / 2, space / 10,
                                        #                '{} / {}'.format(n_current_page, n_page))
                                        pages.showPage()
                                        n_current_page += 1
                                    pages.drawImage(ImageReader(input_dir + '/' + image), space + col * iW, pH - (space + lig * iH + iH), iW, iH)
                                    col += 1
        pages.save()

genBilder = ''
while genBilder != 'J' and genBilder != 'n':
    genBilder = input('Würden Sie erneut die zu den zu generierenden Pdf-Daten entsprechenden Bilder generieren? (J / n)')
if genBilder == 'J':
    gen_images(vp_select = 2)
gen_pdf_images()