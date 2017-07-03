import matplotlib.pylab as plt
import numpy as np
import matplotlib.animation as animation
from config import Config as cfg
import tools as tls
import pandas as pd
import os
from sklearn.metrics import silhouette_score

df = pd.read_csv('/home/herval/Documents/THB/Master/Semester1/Projekt1/DataMining/Eyetracking/data/processed/clustering/cluster.csv', sep=cfg.sep)

clusters = df['cluster'].values
X = df.values[:, :(np.size(df.values, axis=1) - 1)]

for i in range(len(clusters)):
    clusters[i] = int(tls.remove_begin('cluster_', clusters[i]))

print(silhouette_score(X, clusters))