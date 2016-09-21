#!/usr/bin/python

# Simple test uses just the timepoing of weibo

import pandas as pd
import numpy as np
from collections import Counter
from weibo import Weibo

FILE_PATH='/home/hp/Documents/DeepLearning/DataCastle/Weibo/Data/testRepostBeforeFirstHour.txt'

# Data importer
def data_import(file_path):
    origin = pd.read_csv(file_path, sep='\001', header=None)
    weibos = []
    weibo_ids = origin.iloc[:,0].values
    print(Counter(weibo_ids)['testWeibo1'])
    weibo_author_ids = origin.iloc[:,1].values
    weibo_reauthor_ids = origin.iloc[:,2].values
    weibo_timepoints = origin.iloc[:,3].values
    for i in range(origin.shape[0]):
        my_weibo = Weibo(weibo_ids[i], weibo_author_ids[i], weibo_reauthor_ids[i], weibo_timepoints[i])
        weibos.append(my_weibo)
    return weibos
    
def main():
    weibos = data_import(FILE_PATH)

if __name__=='__main__':
    main()
