import pandas as pd


data = pd.read_csv('Book1.csv')

for var in ['main_dep', 'desc_dep', 'main_arr', 'desc_arr']:
    for cat in data[var].unique():
        data[var+"_"+cat] = (data[var] == cat).astype(int)

data.to_csv('Book2.csv', index=False)
