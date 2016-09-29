#!/usr/bin/python

# Simple test uses just the timepoing of weibo
from collections import defaultdict

import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import pickle

from repost_record import RepostRecord

FILE_PATH = '/home/hp/Documents/DeepLearning/DataCastle/Weibo/Data/testRepostBeforeFirstHour.txt'
FILE_PATH2 = '/home/hp/Documents/DeepLearning/DataCastle/Weibo/Data/testRepostBeforeFirstHour900_969.txt'


# Data importer
def data_import():
    origin = pd.read_table(FILE_PATH, sep='\001', header=None, usecols=[0, 1, 2, 3])
    print(origin.shape)
    repost_records = []
    weibo_ids = origin.iloc[:, 0].values
    weibo_author_ids = origin.iloc[:, 1].values
    weibo_reauthor_ids = origin.iloc[:, 2].values
    weibo_timepoints = origin.iloc[:, 3].values
    for i in range(origin.shape[0]):
        repost_record = RepostRecord(weibo_ids[i], weibo_author_ids[i], weibo_reauthor_ids[i], weibo_timepoints[i])
        repost_records.append(repost_record)
    origin2 = pd.read_table(FILE_PATH2, sep='\001', header=None, usecols=[0, 1, 2, 3])
    print(origin2.shape)
    weibo_ids = origin2.iloc[:, 0].values
    weibo_author_ids = origin2.iloc[:, 1].values
    weibo_reauthor_ids = origin2.iloc[:, 2].values
    weibo_timepoints = origin2.iloc[:, 3].values
    for i in range(origin2.shape[0]):
        repost_record = RepostRecord(weibo_ids[i], weibo_author_ids[i], weibo_reauthor_ids[i], weibo_timepoints[i])
        repost_records.append(repost_record)
    print(len(repost_records))
    return repost_records


def calc_breadth(repost_records):
    weibo_repostnum_dict = defaultdict(list)
    weibo_counter_dict = defaultdict(list)
    for i in range(len(repost_records)):
        weibo_repostnum_dict[repost_records[i].weibo_id].append(repost_records[i].weibo_timepoint)
    for i in range(1, 3001):
        weibo_id = 'testWeibo' + str(i)
        time_point = weibo_repostnum_dict[weibo_id]
        weibo_num = [x + 1 for x in range(len(weibo_repostnum_dict[weibo_id]))]
        for t, n in zip(time_point, weibo_num):
            weibo_counter_dict[weibo_id].append((t, n))
    return weibo_counter_dict


def calc_deepth(repost_records):
    weibo_repostdeepth_dict = defaultdict(list)
    i = 0
    g = nx.DiGraph()
    g.add_node(0)
    weibo_start_id = repost_records[i].weibo_id
    weibo_start_author_id = repost_records[i].weibo_author_id
    weibo_author_id = repost_records[i].weibo_author_id
    weibo_reauthor_id = repost_records[i].weibo_reauthor_id
    g.add_edge(0, weibo_author_id)
    g.add_edge(weibo_author_id, weibo_reauthor_id)
    weibo_repostdeepth_dict[repost_records[i].weibo_id].append((repost_records[i].weibo_timepoint,
                                                                int(nx.eccentricity(g, v=0)) - 1))
    i += 1
    while i != len(repost_records) - 1:
        weibo_cur_id = repost_records[i].weibo_id
        weibo_author_id = repost_records[i].weibo_author_id
        weibo_reauthor_id = repost_records[i].weibo_reauthor_id
        if weibo_start_id == weibo_cur_id:
            if weibo_author_id not in g.nodes():
                g.add_edge(weibo_start_author_id, weibo_author_id)
            if weibo_reauthor_id not in g.nodes():
                g.add_edge(weibo_author_id, weibo_reauthor_id)
            weibo_repostdeepth_dict[repost_records[i].weibo_id].append((repost_records[i].weibo_timepoint,
                                                                        int(nx.eccentricity(g, v=0)) - 1))
        else:
            g.clear()
            g.add_node(0)
            weibo_start_id = repost_records[i].weibo_id
            weibo_start_author_id = repost_records[i].weibo_author_id
            weibo_author_id = repost_records[i].weibo_author_id
            weibo_reauthor_id = repost_records[i].weibo_reauthor_id
            g.add_edge(0, weibo_author_id)
            g.add_edge(weibo_author_id, weibo_reauthor_id)
        i += 1
    return weibo_repostdeepth_dict


def save_plot_breadth(weibo_counter_dict):
    with open('weibo_counter_dict.pickle', 'wb') as handle:
        pickle.dump(weibo_counter_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    for i in range(1, 3001):
        weibo_id = 'testWeibo' + str(i)
        axis_x = []
        axis_y = []
        for x, y in weibo_counter_dict[weibo_id]:
            axis_x.append(x)
            axis_y.append(y)
        plt.plot(axis_x, axis_y)
    plt.savefig('weibo_counter.png')


def save_plot_deepth(weibo_repostdeepth_dict):
    with open('weibo_repostdeepth_dict.pickle', 'wb') as handle:
        pickle.dump(weibo_repostdeepth_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    for i in range(1, 3001):
        weibo_id = 'testWeibo' + str(i)
        axis_x = []
        axis_y = []
        for x, y in weibo_repostdeepth_dict[weibo_id]:
            axis_x.append(x)
            axis_y.append(y)
        plt.plot(axis_x, axis_y)
    plt.savefig('weibo_repostdeepth.png')


def main():
    repost_records = data_import()
    weibo_counter_dict = calc_breadth(repost_records)
    save_plot_breadth(weibo_counter_dict)
    weibo_repostdeepth_dict = calc_deepth(repost_records)
    save_plot_deepth(weibo_repostdeepth_dict)

if __name__ == '__main__':
    main()
