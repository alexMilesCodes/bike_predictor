import pandas as pd
from sklearn import model_selection
from xgboost import XGBClassifier


features = ["no_stages", "14_perc_climb_steep", "clouds",
            "yday", "Cobbled?", "WT?", "10_abs_grad", "stage",
            "10_max_grad", "qual", "humidity", "10_climbing_mtrs",
            "wind_speed", "date_#", "4_perc_climb_steep",
            "0_perc_climb_steep", "10_max_alt", "0_abs_grad",
            "14_abs_grad", "Distance", "0_climbing_mtrs",
            "4_max_grad", "coord_dist"]

params = {'min_child_weight': [1, 5, 10],
          'gamma': [0.5, 1, 1.5, 2, 5],
          'subsample': [0.6, 0.8, 1.0],
          'colsample_bytree': [0.6, 0.8, 1.0],
          'max_depth': [3, 4, 5]}

results = pd.read_csv('Results.csv').set_index('Race')
results = results[results['rider'] == 'tadej-pogacar']
data = results.join(pd.read_csv('Basefile1.csv').set_index('Race')).reset_index()
data['performance'] = data['performance'] >= data['performance'].median()

X = data[features]
y = data['performance'].astype(int)

grid = model_selection.GridSearchCV(XGBClassifier(learning_rate=0.02,
                                                  n_estimators=600,
                                                  objective='binary:logistic'),
                                    param_grid=params, cv=5,
                                    verbose=3, scoring='roc_auc')
grid.fit(X, y)

print('\n best score')
print(grid.best_score_)
print('\n best hyperparameters:')
print(grid.best_params_)
