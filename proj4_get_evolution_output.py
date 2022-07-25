import pandas as pd
import numpy as np


data = pd.read_csv('iteration_10.csv')
data.rename(columns={'probability': '10'}, inplace=True)
for i in np.arange(20, 90, 10):
    data[str(i)] = pd.read_csv(f'iteration_{i}.csv')['probability']

data.to_csv('evolution.csv', index=False)
