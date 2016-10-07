#!/usr/bin/python

# Import relation data into Neo4j Graph database
import pickle
import pandas as pd
import numpy as np

TR_FEATURE_FILE_PATH = '/home/hp/Documents/DeepLearning/DataCastle/Weibo/castle_weibo/TRweibo_feature.pickle'
TE_FEATURE_FILE_PATH = '/home/hp/Documents/DeepLearning/DataCastle/Weibo/castle_weibo/TEweibo_feature.pickle'
REL_IN_FILE_PATH = '/home/hp/Documents/DeepLearning/DataCastle/Weibo/castle_weibo/weibo_relation_in_degree_dict.pickle'
REL_OUT_FILE_PATH = \
    '/home/hp/Documents/DeepLearning/DataCastle/Weibo/castle_weibo/weibo_relation_out_degree_dict.pickle'
TRAIN_BREADTH_DEEPTH_FILE_PATH = '/home/hp/Documents/DeepLearning/DataCastle/Weibo/Data/trainScaleDepth.csv'


def clean_data_import_from_pickle():
    with open(TR_FEATURE_FILE_PATH, 'rb') as handle:
        tr_feature = pickle.load(handle)
    tr_feature = pd.DataFrame(np.reshape(tr_feature, [-1, 8]),
                              columns=['weiboid', 'authorid', 'time_period', 'weibo_length',
                                       'topics_num', 'mention_num', 'link_num', 'media_num'])

    with open(TE_FEATURE_FILE_PATH, 'rb') as handle:
        te_feature = pickle.load(handle)
    te_feature = pd.DataFrame(np.reshape(te_feature, [-1, 8]),
                              columns=['weiboid', 'authorid', 'time_period', 'weibo_length',
                                       'topics_num', 'mention_num', 'link_num', 'media_num'])
    te_feature[['authorid']] = te_feature[['authorid']].astype(int)
    with open(REL_IN_FILE_PATH, 'rb') as handle:
        rel_in_dict = pickle.load(handle)
    rel_in_dict = pd.DataFrame.from_dict(rel_in_dict, 'index').reset_index()
    rel_in_dict.columns = ['authorid', 'fans']

    with open(REL_OUT_FILE_PATH, 'rb') as handle:
        rel_out_dict = pickle.load(handle)
    rel_out_dict = pd.DataFrame.from_dict(rel_out_dict, 'index').reset_index()
    rel_out_dict.columns = ['authorid', 'follows']
    return tr_feature, te_feature, rel_in_dict, rel_out_dict


def breadth_deepth_import_from_csv():
    tr_breadth_deepth = pd.read_csv(TRAIN_BREADTH_DEEPTH_FILE_PATH)
    return tr_breadth_deepth


def resave_all_to_csv(merge):
    merge.to_csv('train.csv', index=False)


def resave_test_to_csv(merge):
    merge.to_csv('test.csv', index=False)


def main():
    tr_feature, te_feature, rel_in_dict, rel_out_dict = clean_data_import_from_pickle()
    tr_breadth_deepth = breadth_deepth_import_from_csv()
    merge1 = pd.merge(tr_feature, tr_breadth_deepth, how='left', on='weiboid')
    merge2 = pd.merge(merge1, rel_in_dict, how='left', on='authorid')
    merge3 = pd.merge(merge2, rel_out_dict, how='left', on='authorid')
    scales = []
    for col in ['scaleT' + str(i) for i in range(75, 4381, 15)]:
        scales_log = np.log(merge3[col] + 1)
        if np.sum(scales_log) != 0:
            scales += scales_log.tolist()
        merge3.drop(col, axis=1, inplace=True)
    scales = np.reshape(np.transpose(np.reshape(scales, [288, -1])), [1, -1])[0].tolist()
    print(len(scales))
    depths = []
    for col in ['depthT' + str(i) for i in range(75, 4381, 15)]:
        depths += np.log(merge3[col] + 1).tolist()
        merge3.drop(col, axis=1, inplace=True)
    depths = np.reshape(np.transpose(np.reshape(depths, [288, -1])), [1, -1])[0].tolist()
    print(len(depths))
    merge3['key'] = pd.Series([1] * len(merge3), index=merge3.index)
    times = {'key': [1] * 288, 'time': [i for i in range(75, 4381, 15)]}
    times = pd.DataFrame.from_dict(times)
    merge4 = pd.merge(merge3, times, on='key')
    merge4['scales'] = pd.Series(scales, index=merge4.index)
    merge4['depths'] = pd.Series(depths, index=merge4.index)
    merge4.drop('key', axis=1, inplace=True)
    print(len(merge4))
    print(merge4.columns)
    resave_all_to_csv(merge4)

    merge1 = pd.merge(te_feature, rel_in_dict, how='left', on='authorid')
    merge2 = pd.merge(merge1, rel_out_dict, how='left', on='authorid')
    merge2['key'] = pd.Series([1] * len(merge2), index=merge2.index)
    times = {'key': [1] * 288, 'time': [i for i in range(75, 4381, 15)]}
    times = pd.DataFrame.from_dict(times)
    merge3 = pd.merge(merge2, times, on='key')
    merge3.drop('key', axis=1, inplace=True)
    print(len(merge3))
    print(merge3.columns)
    print(merge3)
    resave_test_to_csv(merge3)


if __name__ == '__main__':
    main()
