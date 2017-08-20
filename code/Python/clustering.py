from config import Config as cfg
import tools as tls
import random

def generate_id():
    ind = list()
    id = ''

    for i in range(ord('0'), ord('9') + 1):
        ind.append(i)

    for i in range(ord('a'), ord('z') + 1):
        ind.append(i)

    for i in range(ord('A'), ord('Z') + 1):
        ind.append(i)

    for j in range(cfg.id_length):
        c = random.randint(0, len(ind) - 1)
        id += chr(ind[c])

    return id

# -*- coding: utf-8 -*-
"""
===================================
Demo of DBSCAN clustering algorithm
===================================

Finds core samples of high density and expands clusters from them.

"""
#print(__doc__)

import numpy as np
import pandas as pd

from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn import preprocessing

#df = pd.read_csv(cfg.resultOhneName)
df = pd.read_csv('/media/herval/Save/School/THB/Master/Semester1/Projekt1/Eyetracking/data/processed/result/result_ohne_korrelierte_merkmale.csv')
X = df.values

scaler = preprocessing.MaxAbsScaler()
X = scaler.fit_transform(X)

sil_max = -100
##############################################################################
# Compute DBSCAN

performance = list()

#for eps in np.arange(0.01, 10, 0.01):
for min_sample in np.arange(2, 20, 1):
    db = KMeans(n_clusters=min_sample, max_iter=10000, init='random', algorithm='elkan', n_init=50).fit(X)
    #core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    #core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    # print('Estimated number of clusters: %d' % n_clusters_)
    #
    try:
        #print("Silhouette Coefficient: %0.3f"
        #       % metrics.silhouette_score(X, labels))
        if sil_max < metrics.silhouette_score(X, labels):
            #e = eps
            s = min_sample
            sil_max = metrics.silhouette_score(X, labels)
        #print("Eps: {}, min_samples: {}".format(e, s))
        db = KMeans(n_clusters=min_sample, max_iter=10000, init='random', algorithm='elkan', n_init=50).fit(X)
        #db = DBSCAN(eps=e, min_samples=s).fit(X)
        #core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        #core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_

        # Number of clusters in labels, ignoring noise if present.
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

        #print('Estimated number of clusters: %d' % n_clusters_)

        #print("Silhouette Coefficient: %0.3f"
        #      % metrics.silhouette_score(X, labels))
        performance.append([db.get_params(), metrics.silhouette_score(X, labels)])
    except:
        pass

id = generate_id()
performDf = pd.DataFrame(np.array(performance), columns=cfg.header_cluster_performance)
performDf.to_csv(cfg.performanceClustering.format(id), index=False, sep=cfg.sep)
#
# print("Eps: {}, min_samples: {}".format(e, s))
#
# db = DBSCAN(eps=e, min_samples=s).fit(X)
# core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
# core_samples_mask[db.core_sample_indices_] = True
# labels = db.labels_
#
# # Number of clusters in labels, ignoring noise if present.
# n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
#
# print('Estimated number of clusters: %d' % n_clusters_)
#
# print("Silhouette Coefficient: %0.3f"
#       % metrics.silhouette_score(X, labels))
##############################################################################
# Plot result
# import matplotlib.pyplot as plt
#
# # Black removed and is used for noise instead.
# unique_labels = set(labels)
# colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
# for k, col in zip(unique_labels, colors):
#     if k == -1:
#         # Black used for noise.
#         col = 'k'
#
#     class_member_mask = (labels == k)
#
#     xy = X[class_member_mask & core_samples_mask]
#     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
#              markeredgecolor='k', markersize=14)
#
#     xy = X[class_member_mask & ~core_samples_mask]
#     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
#              markeredgecolor='k', markersize=6)
#
# plt.title('Estimated number of clusters: %d' % n_clusters_)
# #Nächste Zeile nur in nicht interaktiven Umgebungen nötig
# plt.show()