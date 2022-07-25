import pandas as pd
import numpy as np
from sklearn import ensemble, model_selection


data = pd.read_csv('basefile-6.csv')

n_estimators = [int(x) for x in np.linspace(start=200, stop=2000, num=10)]
max_features = ['auto', 'sqrt']
max_depth = [int(x) for x in np.linspace(10, 110, num=11)]
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

rf_random = model_selection.RandomizedSearchCV(estimator=ensemble.RandomForestRegressor(),
                                               param_distributions=random_grid,
                                               n_iter=100, cv=3, verbose=2, random_state=42,
                                               n_jobs=-1)

for target in ['arr_prcp', 'arr_wpgt']:

    X = data.loc[data[target].notna(), ['arr_lat', 'arr_long', 'arr_alt', 'yday',
                                        'arr_temp', 'arr_dwpt', 'arr_rhum', 'arr_wspd', 'arr_pres']]
    y = data.loc[data[target].notna(), target]

    rf_random.fit(X, y)

    rf = ensemble.RandomForestRegressor()
    rf.set_params(**rf_random.best_params_)
    rf.fit(X, y)

    data.loc[data[target].isna(), target] = rf.predict(data.loc[data[target].isna(),
                                                       ['arr_lat', 'arr_long', 'arr_alt', 'yday',
                                                        'arr_temp', 'arr_dwpt', 'arr_rhum', 'arr_wspd', 'arr_pres']])

data.to_csv('basefile-6.csv', index=False)
