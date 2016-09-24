#!/usr/bin/python

# Simple test uses just the timepoing of weibo
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import pickle

from repost_record import RepostRecord

FILE_PATH = '/home/hp/Documents/DeepLearning/DataCastle/Weibo/Data/testRepostBeforeFirstHour.txt'


# Data importer
def data_import(file_path):
    origin = pd.read_csv(file_path, sep='\001', header=None)
    repost_records = []
    weibo_ids = origin.iloc[:, 0].values
    weibo_author_ids = origin.iloc[:, 1].values
    weibo_reauthor_ids = origin.iloc[:, 2].values
    weibo_timepoints = origin.iloc[:, 3].values
    for i in range(origin.shape[0]):
        repost_record = RepostRecord(weibo_ids[i], weibo_author_ids[i], weibo_reauthor_ids[i], weibo_timepoints[i])
        repost_records.append(repost_record)
    return repost_records


def calc_breadth(repost_records):
    weibo_repostnum_dict = defaultdict(list)
    for i in range(len(repost_records)):
        weibo_repostnum_dict[repost_records[i].weibo_id].append(repost_records[i].weibo_timepoint)
    return weibo_repostnum_dict


def calc_deepth(repost_records, weibo_counter_dict):
    weibo_repostdeepth_dict = defaultdict(list)
    g = nx.Graph()
    diameter = []
    index = 0
    for i in range(1, 3001):
        weibo_id = 'testWeibo' + str(i)
        for j in range(len(weibo_counter_dict[weibo_id])):
            g.add_edge(repost_records[index].weibo_author_id, repost_records[index].weibo_reauthor_id)
            graphs = list(nx.connected_component_subgraphs(g))
            for k in range(len(graphs)):
                diameter.append(nx.diameter(graphs[k]))
            weibo_repostdeepth_dict[repost_records[index].weibo_id].append((repost_records[index].weibo_timepoint,
                                                                            max(diameter)))
            index += 1
        g.clear()
        diameter = []
    return weibo_repostdeepth_dict


def main():
    repost_records = data_import(FILE_PATH)
    weibo_counter_dict = calc_breadth(repost_records)
    with open('weibo_counter_dict.pickle', 'wb') as handle:
        pickle.dump(weibo_counter_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    for i in range(1, len(weibo_counter_dict) + 1):
        weibo_id = 'testWeibo' + str(i)
        axis_x = weibo_counter_dict[weibo_id]
        axis_y = [x + 1 for x in range(len(weibo_counter_dict[weibo_id]))]
        plt.plot(axis_x, axis_y)
    plt.savefig('weibo_counter.png')
    weibo_repostdeepth_dict = calc_deepth(repost_records, weibo_counter_dict)
    with open('weibo_repostdeepth_dict.pickle', 'wb') as handle:
        pickle.dump(weibo_repostdeepth_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    for i in range(1, len(weibo_repostdeepth_dict) + 1):
        weibo_id = 'testWeibo' + str(i)
        axis_x2 = []
        axis_y2 = []
        for x, y in weibo_repostdeepth_dict[weibo_id]:
            axis_x2.append(x)
            axis_y2.append(y)
            plt.plot(axis_x2, axis_y2)
    plt.savefig('weibo_repostdeepth.png')


if __name__ == '__main__':
    main()
