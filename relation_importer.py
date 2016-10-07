#!/usr/bin/python

# Import relation data into Neo4j Graph database
import pickle
import re
from collections import defaultdict

# Real data
FILE_PATH = '/home/hp/Documents/DeepLearning/DataCastle/Weibo/Data/weibo_dc_parse2015_link_filter'
# Sampled file from real data for test purpose
TEST_FILE_PATH = '/home/hp/Documents/DeepLearning/DataCastle/Weibo/Data/relationshiptest.txt'
# Just using bloggers' id in those files
TR_BLOGGERS_FILE_PATH = '/home/hp/Documents/DeepLearning/DataCastle/Weibo/castle_weibo/TRweibo_feature.pickle'
TE_BLOGGERS_FILE_PATH = '/home/hp/Documents/DeepLearning/DataCastle/Weibo/castle_weibo/TEweibo_feature.pickle'


def out_degree_calc():
    weibo_relation_out_degree_dict = defaultdict(int)
    # Progress indicator
    index = 0
    sep = re.compile('\001|\t')
    blogger_ids = set()
    with open(TR_BLOGGERS_FILE_PATH, 'rb') as handle:
        tr_weibo_features = pickle.load(handle)
    with open(TE_BLOGGERS_FILE_PATH, 'rb') as handle:
        te_weibo_features = pickle.load(handle)
    for feature in tr_weibo_features:
        # Blogger id is in the second col
        blogger_ids.add(feature[1])
    for feature in te_weibo_features:
        # Blogger id is in the second col
        blogger_ids.add(feature[1])
    print('Bloggers have been imported, the length is %d' % len(blogger_ids))
    print('Now importe in_degreee...')
    with open(FILE_PATH, 'r') as myfile:
        for l in myfile.readlines():
            arr = sep.split(l.strip())
            if int(arr[0]) in blogger_ids:
                weibo_relation_out_degree_dict[int(arr[0])] = len(arr) - 1
            index += 1
            # Indicator per 100000 steps
            if index % 100000 == 0:
                print(index)
    print(len(weibo_relation_out_degree_dict))
    with open('weibo_relation_out_degree_dict.pickle', 'wb') as handle:
        pickle.dump(weibo_relation_out_degree_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


def in_degree_calc():
    weibo_relation_in_degree_dict = defaultdict(int)
    # Progress indicator
    index = 0
    sep = re.compile('\001|\t')
    blogger_ids = set()
    with open(TR_BLOGGERS_FILE_PATH, 'rb') as handle:
        tr_weibo_features = pickle.load(handle)
    with open(TE_BLOGGERS_FILE_PATH, 'rb') as handle:
        te_weibo_features = pickle.load(handle)
    for feature in tr_weibo_features:
        # Blogger id is in the second col
        blogger_ids.add(feature[1])
    for feature in te_weibo_features:
        # Blogger id is in the second col
        blogger_ids.add(feature[1])
    print(len(weibo_relation_in_degree_dict))
    print('Bloggers have been imported, the length is %d' % len(blogger_ids))
    print('Now importe in_degreee...')
    with open(FILE_PATH, 'r') as myfile:
        for l in myfile.readlines():
            arr = sep.split(l.strip())
            arr = list(map(int, arr[1:]))
            for a in arr:
                if a in blogger_ids:
                    weibo_relation_in_degree_dict[a] += 1
            index += 1
            # Indicator per 100000 steps
            if index % 100000 == 0:
                print(index)
    print(weibo_relation_in_degree_dict[2724513])
    print(len(weibo_relation_in_degree_dict))
    with open('weibo_relation_in_degree_dict.pickle', 'wb') as handle:
        pickle.dump(weibo_relation_in_degree_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


# def convert_to_csv():
#     # progress indicator
#     index = 0
#     sep = re.compile('\001|\t')
#     with open('relationshiptest.csv', 'w') as outfile:
#         writer = csv.writer(outfile, delimiter=',')
#         with open(FILE_PATH, 'r') as myfile:
#             for l in myfile.readlines():
#                 arr = sep.split(l.strip())
#                 writer.writerow(arr)
#                 index += 1
#                 # print per 100000 steps
#                 if index % 100000 == 0:
#                     print(index)


def main():
    out_degree_calc()
    in_degree_calc()


if __name__ == '__main__':
    main()
