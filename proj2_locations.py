import pandas as pd
import geopy as geo
from math import sin, cos, sqrt, atan2, radians


# function to calculate km between locations
def dist_calc(lat1, lon1, lat2, lon2, r=6373.0):

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return r * c


data = pd.read_csv('basefile.csv').sort_values(by=['Race'])
data['date'] = pd.to_datetime(data['date'])

for i in data.index:
    data.loc[i, 'dep'] = data.loc[i, 'dep'].replace('-', ' ')
    data.loc[i, 'arr'] = data.loc[i, 'arr'].replace('-', ' ')

# logic for dealing with nas:
if sum(data['date'].isna()) > 0:
    print('number of NA dates:')
    print(sum(data['date'].isna()))

geo_loc = geo.geocoders.Nominatim(user_agent="locations")

dep_lat = []
dep_long = []
arr_lat = []
arr_long = []
dist = []
check = []
for race in data.index:
    data.loc[race, 'dep'] = ''.join([i for i in data.loc[race, 'dep'] if not i.isdigit()])
    data.loc[race, 'arr'] = ''.join([i for i in data.loc[race, 'arr'] if not i.isdigit()])
    try:
        dep_lat.append(geo_loc.geocode(data['dep'][race]).latitude)
    except:
        dep_lat.append('')
    try:
        dep_long.append(geo_loc.geocode(data['dep'][race]).longitude)
    except:
        dep_long.append('')
    try:
        arr_lat.append(geo_loc.geocode(data['arr'][race]).latitude)
    except:
        arr_lat.append('')
    try:
        arr_long.append(geo_loc.geocode(data['arr'][race]).longitude)
    except:
        arr_long.append('')

    try:
        dist.append(dist_calc(radians(dep_lat[len(dep_lat)-1]),
                              radians(dep_long[len(dep_long)-1]),
                              radians(arr_lat[len(arr_lat)-1]),
                              radians(arr_long[len(arr_long)-1])))
    except:
        dist.append('')
    try:
        check.append(dist_calc(radians(arr_lat[len(arr_lat)-2]),
                               radians(arr_long[len(arr_long)-2]),
                               radians(arr_lat[len(arr_lat)-1]),
                               radians(arr_long[len(arr_long)-1])))
    except:
        check.append('')

    print(f'{list(data.index).index(race)+1}/{len(data.index)}')

data['dep_lat'] = dep_lat
data['dep_long'] = dep_long
data['arr_lat'] = arr_lat
data['arr_long'] = arr_long
data['Location Distance'] = dist
data['Check Distance'] = check

data.to_csv('basefile-3.csv', index=False)
