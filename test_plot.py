import matplotlib.pyplot as plt
import pickle

with open('weibo_repostdeepth_dict.pickle', 'rb') as handle:
    weibo_repostdeepth_dict = pickle.load(handle)
for i in range(1, len(weibo_repostdeepth_dict) + 1):
    weibo_id = 'testWeibo' + str(i)
    axis_x2 = []
    axis_y2 = []
    for x, y in weibo_repostdeepth_dict[weibo_id]:
        axis_x2.append(x)
        axis_y2.append(y)
        plt.plot(axis_x2, axis_y2)
plt.show()
