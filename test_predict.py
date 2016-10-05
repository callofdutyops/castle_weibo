import pickle
import numpy as np
from scipy.optimize import curve_fit
from collections import defaultdict
import csv

BREADTH_FILE_PATH = '/home/hp/Documents/DeepLearning/DataCastle/Weibo/castle_weibo/weibo_counter_dict.pickle'
DEEPTH_FILE_PATH = '/home/hp/Documents/DeepLearning/DataCastle/Weibo/castle_weibo/weibo_repostdeepth_dict.pickle'


# Load data (deserialize)
def import_data():
    with open(BREADTH_FILE_PATH, 'rb') as handle:
        weibo_counter_dict = pickle.load(handle)
    with open(DEEPTH_FILE_PATH, 'rb') as handle:
        weibo_repostdeepth_dict = pickle.load(handle)
    return weibo_counter_dict, weibo_repostdeepth_dict


def func_fit_log(x, a, b):
    return a + b * np.log(x)


def predict_breadth(weibo_counter_dict):
    weibo_breadth_pre = defaultdict(list)
    for i in range(1, 3001):
        weibo_id = 'testWeibo' + str(i)
        data = weibo_counter_dict[weibo_id]
        time_points = []
        weibo_nums = []
        for time_point, weibo_num in data:
            time_points.append(time_point)
            weibo_nums.append(weibo_num)
        fitting_parameters, covariance = curve_fit(func_fit_log, time_points, weibo_nums)
        a, b = fitting_parameters
        time_pre = np.linspace(4500, 262800, 288)
        weibo_num_pre = func_fit_log(time_pre, a, b)
        weibo_num_pre = weibo_num_pre.tolist()
        for j in range(len(weibo_num_pre)):
            weibo_num_pre[j] = int(weibo_num_pre[j])
            # If the first predicted value is smaller than the start value
            # then let the first predicted value equal to start value
            # deepth is the same
            if weibo_num_pre[j] < weibo_nums[-1]:
                weibo_num_pre[j] = weibo_nums[-1]
        weibo_breadth_pre[weibo_id] = weibo_num_pre
    return weibo_breadth_pre


def predict_deepth(weibo_repostdeepth_dict):
    weibo_deepth_pre_dict = defaultdict(list)
    for i in range(1, 3001):
        weibo_id = 'testWeibo' + str(i)
        data = weibo_repostdeepth_dict[weibo_id]
        time_points = []
        weibo_deepths = []
        for time_point, weibo_deepth in data:
            time_points.append(time_point)
            weibo_deepths.append(weibo_deepth)
        fitting_parameters, covariance = curve_fit(func_fit_log, time_points, weibo_deepths)
        a, b = fitting_parameters
        time_pre = np.linspace(4500, 262800, 288)
        weibo_deepth_pre = func_fit_log(time_pre, a, b)
        weibo_deepth_pre = weibo_deepth_pre.tolist()
        for j in range(len(weibo_deepth_pre)):
            weibo_deepth_pre[j] = int(weibo_deepth_pre[j])
            if weibo_deepth_pre[j] < weibo_deepths[-1]:
                weibo_deepth_pre[j] = weibo_deepths[-1]
        weibo_deepth_pre_dict[weibo_id] = weibo_deepth_pre
    return weibo_deepth_pre_dict


def save_prediction(weibo_counter_dict, weibo_repostdeepth_dict):
    weibo_breadth_pre = predict_breadth(weibo_counter_dict)
    weibo_deepth_pre_dict = predict_deepth(weibo_repostdeepth_dict)
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
    weibo_counter_dict, weibo_repostdeepth_dict = import_data()
    save_prediction(weibo_counter_dict, weibo_repostdeepth_dict)


if __name__ == '__main__':
    main()
