import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate

profiles = pd.read_csv('profiles-2.csv')


def window(x_in, metric):
    return max(1 - abs(x_in) / metric, 0)


p = {}
for i in range(round(10.01*max(profiles['Distance']))):
    p[str(i)] = []

for i in range(len(profiles['0'])):

    # load the lists from profiles
    ox = []
    oy = []
    j = 0
    while str(profiles[str(j)][i]) != 'nan':
        oy.append(profiles[str(j)][i])
        j += 1

    # increment
    inc = profiles['Distance'][i] / (len(oy) - 1)
    for j in range(len(oy)):
        ox.append(j * inc)

    # now set increment as constant
    inc = 181/1364

    # add edges for interpolation
    oy = [oy[0] - ((oy[1] - oy[0]) / (ox[1] - oy[0])) * (ox[0] + 4 * inc)] + oy \
        + [oy[len(oy) - 1] + ((oy[len(oy) - 1] - oy[len(oy) - 2]) / (ox[len(ox) - 1] - ox[len(ox) - 2]))
           * (profiles['Distance'][i] + 4 * inc - ox[len(ox) - 1])]
    ox = [-4 * inc] + ox + [profiles['Distance'][i] + 4 * inc]

    # interpolate
    f = interpolate.interp1d(ox, oy)
    x = np.arange(-3.5 * inc, profiles['Distance'][i] + 4 * inc, 0.1)
    y = f(x)

    # add peaks at extremes to counteract peak-over-smoothing
    # c is a correction factor, how much extra is added on to a peak
    c = 0.4
    for j in np.arange(len(y)-2)+1:
        if (y[j] > y[j-1] and y[j] > y[j+1]) or (y[j] < y[j-1] and y[j] < y[j+1]):
            y[j] += c*(y[j]-(y[j-1]+y[j+1])/2)

    # smooth
    # s corresponds to half the width of the window used in smoothing, in increments
    s1 = 2
    x_new = np.arange(0, profiles['Distance'][i] + 0.1, 0.1)
    y_1 = []
    for j in range(len(x_new)):
        y_add = 0
        div = 0
        for k in range(len(x)):
            y_add += window(x_new[j] - x[k], s1 * inc) * y[k]
            div += window(x_new[j] - x[k], s1 * inc)
        y_1.append(y_add / div)

    # plateau averaging
    x = []
    y = []
    j = 0
    while j < len(oy) - 1:
        temp_x = [ox[j]]
        while oy[j] == oy[j + 1] and j < len(oy) - 2:
            j += 1
            temp_x.append(ox[j])
        x.append(float(np.mean(temp_x)))
        y.append(oy[j])
        j += 1

    # add on edges for interpolation and smoothing
    y = [y[0] - ((y[1]-y[0]) / (x[1]-y[0])) * (x[0] + 4*inc)] + y \
        + [y[len(y)-1] + ((y[len(y)-1]-y[len(y)-2]) / (x[len(x)-1]-x[len(x)-2]))
           * (profiles['Distance'][i] + 4*inc - x[len(x)-1])]
    x = [-4 * inc] + x + [profiles['Distance'][i] + 4 * inc]

    # interpolate
    f = interpolate.interp1d(x, y)
    x = np.arange(-3.5*inc, profiles['Distance'][i]+4*inc, 0.1)
    y = f(x)

    # smooth
    s2 = 0.8
    y_2 = []
    for j in range(len(x_new)):
        y_add = 0
        div = 0
        for k in range(len(x)):
            y_add += window(x_new[j] - x[k], s2 * inc) * y[k]
            div += window(x_new[j] - x[k], s2 * inc)
        y_2.append(y_add / div)

    # find a weighted average and find gradients
    y_ave = []
    g = []
    # w=0 means all just smoothed plateau averaged
    # w=1 means all just smoothed original
    w = 0.3
    for j in range(len(x_new)):
        y_ave.append((w*y_1[j] + (1-w)*y_2[j]))
        if j > 0:
            g.append(y_ave[j]-y_ave[j-1])
    g = [g[0]] + g

    # plot
    # fig, ax = plt.subplots(2)
    # ax[0].plot(ox, oy)
    # ax[0].plot(x_new, y_ave)
    # ax[1].plot(x_new, g)
    # plt.show()

    print(len(y_ave))

    for j in range(len(y_ave)):
        p[str(j)].append(y_ave[j])
    for j in range(len(y_ave), round(10.01*max(profiles['Distance']))):
        p[str(j)].append('')

pro_sum = pd.concat([
                        profiles[['Link', 'Race', 'Distance', 'Cobbled?', 'WT?']],
                        pd.DataFrame(p)
                    ], axis=1)

pro_sum.to_csv('profiles_aa.csv', index=False)
