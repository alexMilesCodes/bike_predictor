import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


data = pd.read_csv('profiles_aa.csv')

g_all = []
for race in data.index:
    alt = []
    i = 0
    while str(data.loc[race, str(i)]) != 'nan':
        alt.append(data.loc[race, str(i)])
        i += 1

    g = []
    for i in range(1, len(alt) - 1):
        g.append((alt[i + 1] - alt[i - 1]) / 200)
    g = [g[0]] + g + [g[len(g) - 1]]

    g_all += g

g = pd.Series(g_all)
g_pos = g[np.sign(g) == 1]
g_neg = g[np.sign(g) == -1]
print(f'0.25: {g_pos.quantile(0.25)}')
print(f'median: {g_pos.quantile()}')
print(f'0.75: {g_pos.quantile(0.75)}')
print(f'-ve 0.25: {g_neg.quantile(0.75)}')
print(f'-ve 0.625: {g_neg.quantile(0.375)}')

plt.hist(g, bins=100)
plt.show()
