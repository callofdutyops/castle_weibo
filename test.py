#!/usr/bin/python

# Simple test uses just the timepoing of weibo
from collections import Counter

import pandas as pd
from repost_record import RepostRecord

FILE_PATH = '/home/hp/Documents/DeepLearning/DataCastle/Weibo/Data/testRepostBeforeFirstHour.txt'


# Data importer
def data_import(file_path):
    origin = pd.read_csv(file_path, sep='\001', header=None)
    repost_records = []
    weibo_ids = origin.iloc[:, 0].values
    weibo_counter = Counter(weibo_ids)
    weibo_author_ids = origin.iloc[:, 1].values
    weibo_reauthor_ids = origin.iloc[:, 2].values
    weibo_timepoints = origin.iloc[:, 3].values
    for i in range(origin.shape[0]):
        repost_record = RepostRecord(weibo_ids[i], weibo_author_ids[i], weibo_reauthor_ids[i], weibo_timepoints[i])
        repost_records.append(repost_record)
    return repost_records, weibo_counter


def calc_breadth(repost_records, weibo_counter):
    weibo_counter_dict = {}
    pos = 0
    for i in range(1, 3001):
        weibo_id = 'testWeibo' + str(i)
        count = 0
        timepair = []
        for j in range(weibo_counter[weibo_id]):
            count += 1
            timepair.append((repost_records[pos + j].weibo_timepoint, count))
        weibo_counter_dict[weibo_id] = timepair
        pos = weibo_counter[weibo_id]
    return weibo_counter_dict


def main():
    repost_records, weibo_counter = data_import(FILE_PATH)
    weibo_counter_dict = calc_breadth(repost_records, weibo_counter)
    # print(weibo_counter_dict['testWeibo1'])
    # print(weibo_counter_dict['testWeibo2'])

if __name__ == '__main__':
    main()
