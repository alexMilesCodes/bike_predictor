import pandas as pd
import requests as rs
import numpy as np
import math
from sklearn import linear_model


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


data = pd.read_csv('profiles_aa.csv')

num_sections = 15

phys = []
for i in range(num_sections):
    phys.append({
        'climbing_mtrs': [],
        'abs_grad': [],
        'max_grad': [],
        'max_alt': [],
        'perc_climb_steep': []
    })

won_how = []
vert = []
date = []
start_time = []
ave_spd = []
dep = []
arr = []
rank = []
qual = []
num_start = []
finish_time = []
group_size = []
next_gap = []

count_empty = 0

for race in data.index:
    won_how.append(value_extract(rs.get(data.loc[race, 'Race']).text, 'Won how: </div> <div>', '</div>'))
    vert.append(value_extract(rs.get(data.loc[race, 'Race']).text, 'Vert. meters:</div> <div>', '</div>'))
    date.append(value_extract(rs.get(data.loc[race, 'Race']).text, 'Date:</div> <div>', '</div>'))
    start_time.append(value_extract(rs.get(data.loc[race, 'Race']).text, 'Start time:</div> <div>', '<'))
    ave_spd.append(value_extract(rs.get(data.loc[race, 'Race']).text, 'Avg. speed winner:</div> <div>', ' km/h'))
    dep.append(value_extract(rs.get(data.loc[race, 'Race']).text, 'Departure:</div> <div><a    href="location/', '">'))
    arr.append(value_extract(rs.get(data.loc[race, 'Race']).text, 'Arrival:</div> <div><a    href="location/', '">'))
    rank.append(value_extract(rs.get(data.loc[race, 'Race']).text, 'Race ranking:</div> <div>', '</div>'))
    qual.append(value_extract(rs.get(data.loc[race, 'Race']).text, 'startlist/lineup-quality">', '</a>'))

    # list of riders
    riders = []
    no_time = 0
    check = True
    rdr, t = value_extract(rs.get(data.loc[race, 'Race']).text, 'href="rider/', '">', cut=True)
    while riders.count(rdr) == 0:
        if check:
            riders.append(rdr)
        # check if the next rider is DNS
        check = t[:t.find('href="rider/')].find('<td>DNS</td>') == -1
        if t[:t.find('href="rider/')].find('<td>DNF</td>') != -1\
           or t[:t.find('href="rider/')].find('<td>OTL</td>') != -1:
            no_time += 1
        rdr, t = value_extract(t, 'href="rider/', '">', cut=True)
    print(data.loc[race, 'Race'])
    print(riders)
    num_start.append(len(riders))

    # ADD LOGIC TO ALLOW FOR RIDER POSITION TO BE A TARGET
    # ****************************************************************************************************************

    # ****************************************************************************************************************

    # times (finish_time, group_size & next_gap)
    times = []
    time, t = value_extract(rs.get(data.loc[race, 'Race']).text, 'class="time ar" >', '<', cut=True)
    time, t = value_extract(t, 'class="time ar" >', '<', cut=True)
    i = 0
    while t.find('class="time ar" ><span>') > -1 and i < len(riders)-no_time:
        times.append(time)
        time, t = value_extract(t, 'class="time ar" ><span>', '<', cut=True)
        i += 1
    finish_time.append(times[0])
    i = 1
    while times[i] == ',,' and i < len(times)-1:
        i += 1
    group_size.append(i)
    next_gap.append(times[i])
    print(times)
    # get altitude profile from data
    alt = []
    i = 0
    while str(data.loc[race, str(i)]) != 'nan':
        alt.append(data.loc[race, str(i)])
        i += 1

    # split into the lists
    alt = [
        alt,
        alt[math.floor(0.75*(len(alt))):],
        alt[:math.floor(0.2*(len(alt)))],
        alt[math.floor(len(alt)-50):]
    ]

    for i in range(num_sections):
        # extract gradient from alt[i]
        g = []
        for j in range(1, len(alt[i])-1):
            g.append((alt[i][j+1]-alt[i][j-1])/200)
        g = [g[0]] + g + [g[len(g)-1]]
        mtrs = 0
        for j in range(len(g)-1):
            if g[j] > 0:
                mtrs += g[j]*100
        phys[i]['climbing_mtrs'].append(mtrs)
        phys[i]['abs_grad'].append(np.mean([abs(ele) for ele in g]))
        phys[i]['max_grad'].append(max(g))
        phys[i]['max_alt'].append(max(alt[i]))
        num = 0
        for j in range(len(g)):
            if g[j] >= 0.0342:
                num += 1
        phys[i]['perc_climb_steep'].append(num/(len(g)))
    print(len(vert))
    print(count_empty)

x_dict = {}
for i in range(num_sections):
    for col in phys[i].keys():
        x_dict[f'{str(i)}_{col}'] = phys[i][col]

x_dict['finish_time'] = finish_time
x_dict['group_size'] = group_size
x_dict['next_gap'] = next_gap
x_dict['Race'] = data['Race']
x_dict['Distance'] = data['Distance']
x_dict['Cobbled?'] = data['Cobbled?']
x_dict['WT?'] = data['WT?']
x_dict['vert'] = vert

data = pd.DataFrame(x_dict)

data['Won how?'] = won_how
data['date'] = date
data['start_time'] = start_time
data['ave_spd'] = ave_spd
data['dep'] = dep
data['arr'] = arr
data['rank'] = rank
data['qual'] = qual

times = []
gaps = []
for i in data.index:
    try:
        times.append(int(data.loc[i, 'finish_time'][0])*60*60 +
                     int(data.loc[i, 'finish_time'][2:4])*60 +
                     int(data.loc[i, 'finish_time'][5:]))
    except:
        times.append(data.loc[i, 'finish_time'])
    # if data.loc[i, 'next_gap'] != ',,':
    try:
        gaps.append(int(data.loc[i, 'next_gap'][0])*60 +
                    int(data.loc[i, 'next_gap'][2:]))
    except:
        gaps.append(data.loc[i, 'next_gap'])
data['finish_time'] = times
data['next_gap'] = gaps

data.to_csv('basefile_V3.csv', index=False)
