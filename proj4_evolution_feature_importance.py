import pandas as pd
import numpy as np
from sklearn import model_selection, linear_model, inspection
# from catboost import CatBoostClassifier


base = pd.read_csv('Basefile1.csv').set_index('Race')
results = pd.read_csv('Results.csv').set_index('Race')
results = results[results['rider'].notna()]

full = ['0_climbing_mtrs', '0_abs_grad', '0_max_grad',
            '0_max_alt', '0_perc_climb_steep', '4_climbing_mtrs',
            '4_abs_grad', '4_max_grad', '4_max_alt',
            '4_perc_climb_steep', '10_climbing_mtrs',
            '10_abs_grad', '10_max_grad', '10_max_alt',
            '10_perc_climb_steep', '14_climbing_mtrs', '14_abs_grad',
            '14_max_grad', '14_max_alt', '14_perc_climb_steep',
            'no_stages', 'stage', 'Distance',
            'rank', 'qual', 'Cobbled?',
            'WT?', 'date_#', 'yday',
            'start_time_#', 'coord_dist', 'temp',
            'feels_like', 'pressure', 'humidity',
            'dew_point', 'clouds', 'wind_speed']

for var in full:
    base[var] = (base[var]-base[var].min())/(base[var].max()-base[var].min())

reduced = full.copy()
for var in ['0_max_grad', '14_max_alt', '14_perc_climb_steep',
            'feels_like', '10_max_alt', 'clouds', 'yday',
            'Cobbled?', 'temp', 'wind_speed', 'pressure',
            'start_time_#', 'WT?']:
    reduced.remove(var)

reduced_2 = full.copy()
for var in [["0_max_alt", "0_max_grad", "10_perc_climb_steep",
             "14_climbing_mtrs", "14_max_alt", "14_max_grad",
             "4_abs_grad", "4_climbing_mtrs", "4_max_alt",
             "4_max_grad", "coord_dist", "dew_point",
             "Distance", "feels_like", "rank",
             "start_time_#", "temp"]]:
    reduced_2.remove(var)

prob = np.ones(len(full))*40
score = []
for n in range(500):
    # select features
    features = []
    while len(features) < 1:
        for v in range(len(full)):
            if np.random.random()*100 < prob[v]:
                features.append(full[v])

    # train models§
    train = []
    test = []
    diff = np.zeros(len(full))
    for rider in results['rider'].unique():
        if results['rider'].value_counts()[rider] > len(features)*5:

            data = results[results['rider'] == rider].join(base)
            X = data[features]
            y = (data['performance'] > data['performance'].median()).astype(int)

            X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.25)

            # model = CatBoostClassifier(verbose=False, od_type='IncToDec', od_pval=0.01)
            # model.fit(X_train, y_train, eval_set=(X_test, y_test))

            model = linear_model.LogisticRegression()
            model.fit(X_train, y_train)

            train.append(model.score(X_train, y_train))
            test.append(model.score(X_test, y_test))

            # update probability differences for importance
            model.fit(X, y)
            result = inspection.permutation_importance(model, X, y, n_repeats=10).importances_mean
            i = 0
            for var in features:
                if result[i] > np.median(result):
                    diff[full.index(var)] += 1
                elif result[i] < np.median(result):
                    diff[full.index(var)] -= 1
                i += 1

    # print performance
    print(f'number of riders: {len(train)}, average train score: {np.mean(train)}, average test score: {np.mean(test)}')
    score.append(np.mean(test))

    # update probabilities for importance
    prob += diff/len(train)

    # update probabilities for test score
    if np.mean(test) > np.median(score):
        for var in features:
            prob[full.index(var)] += 1
    if np.mean(test) < np.median(score):
        for var in features:
            prob[full.index(var)] -= 1

    # add on adjustment
    prob += 40-np.mean(prob)

    if n % 10 == 9:
        output = pd.DataFrame({'feature': full, 'probability': prob})
        output.to_csv(f'iteration_{(n+1)}.csv', index=False)
