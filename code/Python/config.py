import numpy as np

class Config:
    #Paths
    root = './../../'
    rawDataHome = root + 'data/raw/DatenTHB/'
    exploratoryHome = root + 'figures/exploratory/'
    finalHome = root + 'figures/final/'
    processedHome = root + 'data/processed/'
    resultHome = processedHome + 'result/'
    matchedHome = processedHome + 'matched/'
    extendedHome = processedHome + 'extended/'
    datenZerlegungHome = processedHome + 'daten_zerlegung/'
    visualisierungBilderHome = exploratoryHome + 'visualisierungBilder/'
    visualisierungPdfHome = exploratoryHome + 'visualisierungPdf/'

    #Excludes
    exclude = ['131']

    #Origin
    o_prim = np.array([640, 512])
    o = np.array([0, 0])

    #Variable
    experimente = ['liegende_acht_langsam', 'liegende_acht_schnell', 'horizontal']
    messungen = ['messung1', 'messung2', 'probe']
    cycles = ['cycle1', 'cycle2']
