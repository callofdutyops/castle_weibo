from collections import defaultdict

import pandas as pd
import xgboost as xgb
import pickle

import numpy as np
from sklearn.cross_validation import KFold
from sklearn.metrics import mean_squared_error

rng = np.random.RandomState(31337)

# load dataset
train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test.csv')
train_ds = train_df.values
test_ds = test_df.values

# split into input (X) and output (Y) variables
X = train_ds[0:100000, 2:11]
y_sc = train_ds[0:100000, 11]
y_de = train_ds[0:100000, 12]

X_ = test_ds[:, 2:11]

print("regression...")
kf = KFold(y_sc.shape[0], n_folds=2, shuffle=True, random_state=rng)

max_depths = [10, 15, 20]
learning_rates = [0.1, 0.2, 0.3]
n_estimators = [300, 500, 700]
gammas = [0, 0.1, 0.2]
min_child_weights = [2, 3, 4]
reg_lambdas = [1, 2, 3]
subsamples = [0.7, 0.8, 0.9]

parameters = defaultdict(list)

for max_depth in max_depths:
    for learning_rate in learning_rates:
        for n_estimator in n_estimators:
            for gamma in gammas:
                for min_child_weight in min_child_weights:
                    for reg_lambda in reg_lambdas:
                        for subsample in subsamples:
                            for train_index, test_index in kf:
                                xgb_model = xgb.XGBRegressor(max_depth=max_depth, learning_rate=learning_rate,
                                                             gamma=gamma, min_child_weight=min_child_weight,
                                                             subsample=subsample, n_estimators=n_estimator,
                                                             reg_lambda=reg_lambda).fit(X[train_index],
                                                                                        y_sc[train_index])
                                predictions = xgb_model.predict(X[test_index])
                                actuals = y_sc[test_index]
                                parameters[mean_squared_error(actuals, predictions)] = [max_depth, learning_rate,
                                                                                        n_estimator, gamma,
                                                                                        min_child_weight,
                                                                                        reg_lambda, subsample]
                                with open('parameters.pickle', 'wb') as handle:
                                    pickle.dump(parameters, handle, protocol=pickle.HIGHEST_PROTOCOL)
                                print(str(max_depth) + ' ' + str(learning_rate) + ' ' +
                                      str(n_estimator) + ' ' + str(gamma) + ' ' +
                                      str(min_child_weight) + ' ' +
                                      str(reg_lambda) + ' ' + str(subsample) + ' ' +
                                      str(mean_squared_error(actuals, predictions)))


# predictions = pd.DataFrame(test_ds[:, 0], columns=['weiboid'])
#
# xgb_model = xgb.XGBRegressor(max_depth=20, gamma=0.2, min_child_weight=2,
#                              subsample=0.9, n_estimators=500).fit(X, y_sc)
# sc_pre = xgb_model.predict(X_)
# sc_pre = np.exp(sc_pre)
# sc_pre = sc_pre.astype(int) - 1
#
# xgb_model = xgb.XGBRegressor(max_depth=20, gamma=0.1, min_child_weight=1,
#                              subsample=0.9, n_estimators=1000).fit(X, y_de)
# de_pre = xgb_model.predict(X_)
# de_pre = np.exp(de_pre)
# de_pre = de_pre.astype(int) - 1
#
# predictions['scales'] = pd.Series(sc_pre, index=predictions.index)
# predictions['depth'] = pd.Series(de_pre, index=predictions.index)
# predictions.to_csv('results.csv', index=False)
