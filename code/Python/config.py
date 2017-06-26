import numpy as np
import os

class Config:
    #Paths
    root = os.path.abspath('./../../')
    rawDataHome = os.path.join(root, 'data/raw/DatenTHB/')
    rawDataSoSe2017Home = os.path.join(root, 'data/raw/DatenTHB_SoSe2017/')
    exploratoryHome = os.path.join(root, 'figures/exploratory/')
    finalHome = os.path.join(root, 'figures/final/')
    processedHome = os.path.join(root, 'data/processed/')
    resultHome = os.path.join(processedHome, 'result/')
    resultOhneName = os.path.join(resultHome, 'result_ohne_vp_name.csv')
    performanceClustering = os.path.join(resultHome, 'performance_clustering_{}.csv')
    matchedHome = os.path.join(processedHome, 'matched/')
    extendedHome = os.path.join(processedHome, 'extended/')
    datenZerlegungHome = os.path.join(processedHome, 'daten_zerlegung/')
    visualisierungBilderHome = os.path.join(exploratoryHome, 'visualisierungBilder/')
    visualisierungPdfHome = os.path.join(exploratoryHome, 'visualisierungPdf/')

    #Excludes
    exclude = ['131', '071', '090']

    #Origin
    o_prim = np.array([640, 512])
    o = np.array([0, 0])

    #Variable
    experimente = ['liegende_acht_langsam', 'liegende_acht_schnell', 'horizontal']
    messungen = ['messung1', 'messung2', 'probe']
    cycles = ['cycle1', 'cycle2']
    header_cluster_performance = ['eps', 'min_sample', 'n_cluster', 'silhouette']
    id_length = 10
    sep=','

    #prefix
    prefix = 'vp_'

    #suffix
    suffix = '_gaze.csv'
    gaze = '_gaze'
