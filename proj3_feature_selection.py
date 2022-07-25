import pandas as pd
import numpy as np
from sklearn import ensemble, model_selection, inspection


data = pd.read_csv('/Users/alexmiles/PycharmProjects/bike_team_maker/Book3.csv')

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
                                               n_iter=500, cv=3, verbose=2, random_state=42,
                                               n_jobs=-1)

features = ["0_climbing_mtrs",
            "0_abs_grad",
            "0_max_grad",
            "0_max_alt",
            "0_perc_climb_steep",
            "10_climbing_mtrs",
            "10_abs_grad",
            "10_max_grad",
            "10_max_alt",
            "10_perc_climb_steep",
            "14_climbing_mtrs",
            "14_abs_grad",
            "14_max_grad",
            "14_max_alt",
            "14_perc_climb_steep",
            "no_stages",
            "stage",
            "Distance",
            "rank",
            "qual",
            "Cobbled?",
            "WT?",
            "date_#",
            "start_unix",
            "finish_unix",
            "temp_dep",
            "feels_like_dep",
            "pressure_dep",
            "humidity_dep",
            "dew_point_dep",
            "clouds_dep",
            "wind_speed_dep",
            "temp_arr",
            "feels_like_arr",
            "pressure_arr",
            "humidity_arr",
            "dew_point_arr",
            "clouds_arr",
            "wind_speed_arr",
            "yday",
            "start_time_#",
            "main_dep_Clear",
            "main_dep_Rain",
            "main_dep_Clouds",
            "main_dep_Mist",
            "main_dep_Snow",
            "main_dep_Drizzle",
            "main_dep_Haze",
            "main_dep_Thunderstorm",
            "main_dep_Dust",
            "desc_dep_clear sky",
            "desc_dep_moderate rain",
            "desc_dep_broken clouds",
            "desc_dep_scattered clouds",
            "desc_dep_few clouds",
            "desc_dep_light rain",
            "desc_dep_mist",
            "desc_dep_overcast clouds",
            "desc_dep_light snow",
            "desc_dep_light intensity shower rain",
            "desc_dep_light intensity drizzle",
            "desc_dep_heavy intensity rain",
            "desc_dep_haze",
            "desc_dep_thunderstorm",
            "desc_dep_dust",
            "main_arr_Clear",
            "main_arr_Clouds",
            "main_arr_Rain",
            "main_arr_Drizzle",
            "main_arr_Snow",
            "main_arr_Mist",
            "main_arr_Haze",
            "main_arr_Dust",
            "desc_arr_clear sky",
            "desc_arr_broken clouds",
            "desc_arr_light rain",
            "desc_arr_overcast clouds",
            "desc_arr_few clouds",
            "desc_arr_heavy intensity rain",
            "desc_arr_scattered clouds",
            "desc_arr_light intensity drizzle rain",
            "desc_arr_moderate rain",
            "desc_arr_light snow",
            "desc_arr_mist",
            "desc_arr_light intensity shower rain",
            "desc_arr_shower rain",
            "desc_arr_snow",
            "desc_arr_haze",
            "desc_arr_dust",
            "coord_dist"]

other_targets = ['Won how?']

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

    result = inspection.permutation_importance(rf, X, y, n_repeats=30, random_state=42)

    pd.DataFrame({'feature': features,
                  'mean': result.importances_mean,
                  'std': result.importances_std}).sort_values(['mean']).to_csv(target+'_importance.csv', index=False)
