from sklearn import ensemble
from sklearn import model_selection
import pandas as pd
import numpy as np


data = pd.read_csv('basefile-2.csv').convert_dtypes()

to_rem = ['Race', 'next_gap', 'group_size', 'finish_time',
          'start_time', 'dep_lat', 'dep_long', 'arr_lat', 'arr_long',
          'Location Distance', 'ave_spd', 'Won how?', 'date', 'dep',
          'arr', 'Check Distance']

cols = data.columns.to_list()
for col in to_rem:
    cols.remove(col)

n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
max_features = ['auto', 'sqrt']
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
min_samples_split = [2, 5, 10]
min_samples_leaf = [1, 2, 4]
bootstrap = [True, False]
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}


rf = ensemble.RandomForestRegressor()
rf_random = model_selection.RandomizedSearchCV(estimator=rf, param_distributions=random_grid,
                                               n_iter=100, cv=3, verbose=2, random_state=42,
                                               n_jobs=-1)

targets = ['group_size', 'next_gap', 'finish_time', 'ave_spd']

for log in [True]:
    for target in ['ave_spd']:
        X = np.array(data[(data[target] != ',,') & (data[target] != '') & (data[target].notna())][cols])
        if log:
            y = np.array(np.log(data[(data[target] != ',,') & (data[target] != '') & (data[target].notna())]
                                [target].astype(float)))
        else:
            y = np.array(data[(data[target] != ',,') & (data[target] != '') & (data[target].notna())]
                                [target].astype(float))
        X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.25)
        rf_random.fit(X_train, y_train)
        print(log, target)
        print(rf_random.best_params_)
