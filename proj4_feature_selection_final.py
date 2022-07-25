import pandas as pd
import numpy as np
from sklearn import ensemble, model_selection, inspection


data = pd.read_csv('Basefile1.csv').set_index('Race')
data = data.join(pd.read_csv('Outcomes.csv').set_index('Race')).reset_index()

n_estimators = [int(x) for x in np.linspace(start=200, stop=2000, num=10)]
max_features = [1.0, 'sqrt']
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
                                               n_iter=100, cv=3, verbose=2, n_jobs=-1)

features = ['0_climbing_mtrs', '0_abs_grad', '0_max_grad',
            '0_max_alt', '0_perc_climb_steep', '10_climbing_mtrs',
            '10_abs_grad', '10_max_grad', '10_max_alt',
            '10_perc_climb_steep', '14_climbing_mtrs', '14_abs_grad',
            '14_max_grad', '14_max_alt', '14_perc_climb_steep',
            'no_stages', 'stage', 'Distance',
            'rank', 'qual', 'Cobbled?',
            'WT?', 'date_#', 'yday',
            'start_time_#', 'coord_dist', 'temp',
            'feels_like', 'pressure', 'humidity',
            'dew_point', 'clouds', 'wind_speed']

for target in ['finish_time', 'group_size', 'next_gap']:

    if target == 'next_gap':
        X = data.loc[data['next_gap'] != ',,', features]
        y = data.loc[data['next_gap'] != ',,', target]
    else:
        X = data[features]
        y = data[target]

    rf_random.fit(X, y)

    rf = ensemble.RandomForestRegressor()
    rf.set_params(**rf_random.best_params_)
    rf.fit(X, y)

    input(rf.score(X, y))

    result = inspection.permutation_importance(rf, X, y, n_repeats=10)

    pd.DataFrame({'feature': features,
                  'mean': result.importances_mean,
                  'std': result.importances_std}).sort_values(['mean']).to_csv(target+'_importance.csv', index=False)
