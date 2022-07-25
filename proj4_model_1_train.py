import pandas as pd
from sklearn import model_selection, linear_model
from xgboost import XGBClassifier


features = ["no_stages", "14_perc_climb_steep", "clouds",
            "yday", "Cobbled?", "WT?", "10_abs_grad", "stage",
            "10_max_grad", "qual", "humidity", "10_climbing_mtrs",
            "wind_speed", "date_#", "4_perc_climb_steep",
            "0_perc_climb_steep", "10_max_alt", "0_abs_grad",
            "14_abs_grad", "Distance", "0_climbing_mtrs",
            "4_max_grad", "coord_dist"]

xgb = XGBClassifier(learning_rate=0.02, n_estimators=600, objective='binary:logistic',
                    colsample_bytree=0.8, gamma=5, max_depth=4,
                    min_child_weight=1, subsample=0.6)

results = pd.read_csv('Results.csv').set_index('Race')
results = results[results['rider'] == 'alejandro-valverde']
data = results.join(pd.read_csv('Basefile1.csv').set_index('Race')).reset_index()
data['top_10'] = data['place'] <= data['place'].median()

X = data[features]
y = data['top_10'].astype(int)

cv_results = model_selection.cross_validate(linear_model.LogisticRegression(),
                                            X, y, scoring='accuracy', return_train_score=True, cv=8)

print(data.shape[0])
print(cv_results['train_score'].mean())
print(cv_results['test_score'].mean())
