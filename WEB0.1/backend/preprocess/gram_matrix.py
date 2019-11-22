import numpy as np
import pandas as pd
import sys, os
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def ESRB_cal(x, y):
    ESRB_dict = {'Unknown': 0, 'KA': -1, 'T': 13, 'E': -
                 1, 'AO': 18, 'EC': 3, 'M': 17, 'RP': -1, 'E10': 10}
    ESRB_all_age_list = ['Unknown', 'KA', 'E', 'EC', 'RP']
    if x in ESRB_all_age_list and y in ESRB_all_age_list:
        return 1
    else:
        temp = abs(ESRB_dict[x] - ESRB_dict[y])
        return 1/temp if temp != 0 else 1
        
def relevance_score_cal():
    gram_matrix = np.zeros((3000, 3000))
    pg = pd.read_csv('../ML/DataSet/KNN.csv')
    pg = pg.head(3000)
    for outer in pg.itertuples():
        ORK = int(outer[1])
        OGE = outer[3]
        OES = outer[4]
        OPL = outer[5]
        OSC = (outer[8], outer[9])
        if OSC[0] * OSC[1] == 0:
            if OSC[0]+OSC[1] == 0:
                OSC = 0
            else:
                OSC = OSC[0] if OSC[1] == 0 else OSC[1]
        else:
            OSC = (OSC[0]+OSC[1])/2
        OSA = outer[10]
        OYE = outer[15]
        for inner in pg.itertuples():
            IRK = int(inner[1])
            IGE = inner[3]
            IES = inner[4]
            IPL = inner[5]
            ISC = (inner[8], inner[9])
            if ISC[0] * ISC[1] == 0:
                if ISC[0]+ISC[1] == 0:
                    ISC = 0
                else:
                    ISC = ISC[0] if ISC[1] == 0 else ISC[1]
            else:
                ISC = (ISC[0]+ISC[1])/2
            ISA = inner[10]
            IYE = inner[15]

            GE = 1 if OGE == IGE else 0
            ES = ESRB_cal(OES, IES)
            PL = 1 if OPL == IPL else 0.8
            SC = sigmoid(1/abs(OSC-ISC)) if OSC != ISC else 1
            temp = abs(OSA-ISA)
            SA = 1 if temp<10 else 0
            YE = 1/abs(OYE-IYE) if OYE != IYE else 1
            relevance_score = GE*ES*PL*SC*SA*YE
            gram_matrix[ORK-1, IRK-1] = relevance_score
        print('Calculation now proceeding...', ORK)
    return gram_matrix


final_matrix = relevance_score_cal()
final_matrix = pd.DataFrame(final_matrix)
final_matrix.to_csv('../ML/DataSet/relevance_matrix.csv')
