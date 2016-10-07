import pandas as pd
import pickle
from collections import defaultdict
import csv

FILE_PATH = '/home/hp/Documents/DeepLearning/DataCastle/Weibo/castle_weibo/results.csv'
BREADTH_FILE_PATH = '/home/hp/Documents/DeepLearning/DataCastle/Weibo/castle_weibo/weibo_counter_dict.pickle'
DEEPTH_FILE_PATH = '/home/hp/Documents/DeepLearning/DataCastle/Weibo/castle_weibo/weibo_repostdeepth_dict.pickle'


# Load data (deserialize)
def import_data():
    with open(BREADTH_FILE_PATH, 'rb') as handle:
        weibo_counter_dict = pickle.load(handle)
    with open(DEEPTH_FILE_PATH, 'rb') as handle:
        weibo_repostdeepth_dict = pickle.load(handle)

    weibo_breadth_pre = defaultdict(list)
    weibo_deepth_pre_dict = defaultdict(list)
    df = pd.read_csv(FILE_PATH)
    ds = df.values
    weiboids = ds[:, 0].tolist()
    breadths = ds[:, 1].tolist()
    deepths = ds[:, 2].tolist()
    for i in range(len(ds)):
        if breadths[i] < weibo_counter_dict[weiboids[i]][-1][1]:
            weibo_breadth_pre[weiboids[i]].append(weibo_counter_dict[weiboids[i]][-1][1])
        else:
            weibo_breadth_pre[weiboids[i]].append(breadths[i])

        if deepths[i] < weibo_repostdeepth_dict[weiboids[i]][-1][1]:
            weibo_deepth_pre_dict[weiboids[i]].append(weibo_repostdeepth_dict[weiboids[i]][-1][1])
        else:
            weibo_deepth_pre_dict[weiboids[i]].append(deepths[i])
    return weibo_breadth_pre, weibo_deepth_pre_dict


def save_prediction(weibo_breadth_pre, weibo_deepth_pre_dict):
    row = ['WeiboID (Time Unit: Minutes)']
    for i in range(75, 4381, 15):
        text = 'scaleT' + str(i)
        row.append(text)
    for i in range(75, 4381, 15):
        text = 'depthT' + str(i)
        row.append(text)
    with open('prediction.csv', 'w') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        writer.writerow(row)
        for i in range(1, 3001):
            weibo_id = 'testWeibo' + str(i)
            row = weibo_breadth_pre[weibo_id]
            row.insert(0, weibo_id)
            row = row + weibo_deepth_pre_dict[weibo_id]
            writer.writerow(row)


def main():
    weibo_breadth_pre, weibo_deepth_pre_dict = import_data()
    save_prediction(weibo_breadth_pre, weibo_deepth_pre_dict)


if __name__ == '__main__':
    main()
