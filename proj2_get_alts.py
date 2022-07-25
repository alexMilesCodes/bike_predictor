import pandas as pd
import numpy as np


prof = pd.read_csv('profiles_aa.csv')
data = pd.read_csv('basefile-4.csv')

dep_alt = []
arr_alt = []
count = 0
for race in data['Race']:
    alt = []
    i = 0
    while str(prof.loc[prof['Race'] == race, str(i)].values[0]) != 'nan':
        alt.append(prof.loc[prof['Race'] == race, str(i)].values[0])
        i += 1
    dep_alt.append(alt[0])
    arr_alt.append(alt[len(alt)-1])
    count += 1
    print(count)

data['dep_alt'] = dep_alt
data['arr_alt'] = arr_alt

data.to_csv('basefile-5.csv', index=False)
