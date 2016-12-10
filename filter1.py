import pandas
import os

verzeichnis = "../2016 - Data Mining Projekt/1 - Aufgabe/DatenTHB/"
dateinamen = os.listdir(verzeichnis)

zielordner = 'zieldateien/'
blickordner = 'blickdateien/'

if os.path.exists(zielordner) == False:
	os.mkdir(zielordner)
if os.path.exists(blickordner) == False:
	os.mkdir(blickordner)

for dateiname in dateinamen:
	if 'gaze' not in dateiname:
		list = pandas.read_csv(verzeichnis + dateiname,sep=";")
		file_ = open(zielordner + dateiname.split('.')[0] + '.csv', 'w')
		file_.write('t_Tracker;pix_x;pix_y\n')
		for i in list.axes[0]: 	#Zeilennummerierung durchgehen
			print(list.at[i,'t_Tracker'])
			file_.write(str(list.at[i,'t_Tracker']))
			file_.write(';')
			file_.write(str(list.at[i,'pix_x']))
			file_.write(';')
			file_.write(str(list.at[i,'pix_y']))
			file_.write('\n')
		file_.close()
	else:
		list = pandas.read_csv(verzeichnis + dateiname,sep=" ")
		file_ = open(blickordner + dateiname.split('.')[0] + '.csv', 'w')
		file_.write('zeitstempel;blick_l_x;blick_l_y;blick_r_x;blick_r_y\n')
		for i in list.axes[0]:  #Zeilennummerierung durchgehen
			print(list.at[i,'zeitstempel'])
			file_.write(str(list.at[i,'zeitstempel']))
			file_.write(';')
			file_.write(str(list.at[i,'blick_l_x']))
			file_.write(';')
			file_.write(str(list.at[i,'blick_l_y']))
			file_.write(';')
			file_.write(str(list.at[i,'blick_r_x']))
			file_.write(';')
			file_.write(str(list.at[i,'blick_r_x']))
			file_.write('\n')
		file_.close()
		
