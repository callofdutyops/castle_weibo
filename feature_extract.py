
import pandas as pd
import pickle
import re
import math
import datetime

FILE_PATH = 'E:\\baiduyundownload\\weibo_DC\\WeiboProfile.test'

feature=[]

origin = pd.read_table(FILE_PATH, sep='\001', header=None, usecols=[0, 1, 2, 3])
weibo_ids = origin.iloc[:, 0].values
author_ids = origin.iloc[:, 1].values
post_time = origin.iloc[:, 2].values
weibo_content = origin.iloc[:, 3].values

for i in range(origin.shape[0]):
    s = weibo_content[i]
    rule1 = re.compile(r'#.*?#') #topics
    rule2 = re.compile(r'@')     #mention
    rule3 = re.compile(r'http')  #links
    rule4 = re.compile(r'\[图片\]|\[音乐\]') #media
    m1 = rule1.findall(s)
    m2 = rule2.findall(s)
    m3 = rule3.findall(s)
    m4 = rule4.findall(s)
    topics_num = len(m1)
    mention_num = len(m2)
    link_num = len(m3)
    media_num = len(m4)

    l = len(s)
    utf8_length = len(s.encode('utf-8'))
    l = (utf8_length - l) / 2 + l
    weibo_length = (math.ceil(l / 2))  #weibo length

    time = post_time[i]
    time = datetime.datetime.strptime(time, '%H:%M:%S')
    t = time.hour
    if t <= 6:
       time_period = 0
    elif t <= 12:
        time_period = 1
    elif t <= 18:
        time_period =2
    else:
        time_period = 3

    feature.append([weibo_ids[i],author_ids[i],time_period,weibo_length,topics_num,mention_num,link_num,media_num])

with open('TEweibo_feature.pickle', 'wb') as handle:
    pickle.dump(feature, handle, protocol=pickle.HIGHEST_PROTOCOL)

