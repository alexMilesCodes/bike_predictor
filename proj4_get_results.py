import pandas as pd
from requests import get
import numpy as np


# define a function that takes in:
#    tem - alias of temp
#    start - string indicating the start of the stat string
#    fin - string indicating the end of the stat string
#    cut - if true, return tem but with the string and everything before removed
# ...and returns the extracted string
def value_extract(tem, start, fin, cut=False):
    te = tem
    da = tem.find(start)
    if da >= 0:
        da += len(start)
        te = tem[da:]
        output = te[:te.find(fin)]
    else:
        output = ''
    if cut:
        return output, te
    else:
        return output


data = pd.read_csv('Basefile1.csv')

rider_lst = []
performance = []
place = []
num_places = []
race_lst = []
for race in data.index:

    # list of riders
    riders = []
    no_time = 0
    check = True
    rdr, t = value_extract(get(data.loc[race, 'Race']).text, 'href="rider/', '">', cut=True)
    while riders.count(rdr) == 0:
        if check:
            riders.append(rdr)
        # check if the next rider is DNS
        check = t[:t.find('href="rider/')].find('<td>DNS</td>') == -1
        if t[:t.find('href="rider/')].find('<td>DNF</td>') != -1\
           or t[:t.find('href="rider/')].find('<td>OTL</td>') != -1:
            no_time += 1
        rdr, t = value_extract(t, 'href="rider/', '">', cut=True)

    for rider in riders:
        rider_lst.append(rider)
        performance.append(np.exp(-54.2*riders.index(rider)/len(riders)))
        place.append(riders.index(rider)+1)
        num_places.append(len(riders))
        race_lst.append(data.loc[race, 'Race'])

data.reset_index('Race', inplace=True)

pd.DataFrame({'Race': race_lst,
              'rider': rider_lst,
              'performance': performance,
              'place': place,
              'num_places': num_places}).to_csv('Results.csv', index=False)
