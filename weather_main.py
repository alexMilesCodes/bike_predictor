import meteostat as mt
import pandas as pd
import geopy as geo
import numpy as np
from math import sin, cos, sqrt, atan2, radians


# function to calculate km between locations
def dist_calc(lat1, lon1, lat2, lon2, r=6373.0):

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) * 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) * 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return r * c


races = pd.read_csv('races.csv')

races = races[(races['Arrival Location'].notna())]

races['Date'] = pd.to_datetime(races['Date'])

# logic for dealing with nas:
if sum(races['Date'].isna()) > 0:
    print('number of NA dates:')
    print(sum(races['Date'].isna()))

geo_loc = geo.geocoders.Nominatim(user_agent="weather_main")

dep_lat = []
dep_long = []
arr_lat = []
arr_long = []
dist = []
for race in races.index:
    races.loc[race, 'Departure Location'] = ''.join([i for i in races.loc[race, 'Departure Location']
                                                     if not i.isdigit()])
    races.loc[race, 'Arrival Location'] = ''.join([i for i in races.loc[race, 'Arrival Location']
                                                    if not i.isdigit()])
    try:
        dep_lat.append(geo_loc.geocode(races['Departure Location'][race]).latitude)
    except:
        dep_lat.append('')
    try:
        dep_long.append(geo_loc.geocode(races['Departure Location'][race]).longitude)
    except:
        dep_long.append('')
    try:
        arr_lat.append(geo_loc.geocode(races['Arrival Location'][race]).latitude)
    except:
        arr_lat.append('')
    try:
        arr_long.append(geo_loc.geocode(races['Arrival Location'][race]).longitude)
    except:
        arr_long.append('')

    try:
        dist.append(dist_calc(radians(dep_lat[len(dep_lat)-1]),
                              radians(dep_long[len(dep_long)-1]),
                              radians(arr_lat[len(arr_lat)-1]),
                              radians(arr_long[len(arr_long)-1])))
    except:
        dist.append('')

    print(f'{list(races.index).index(race)+1}/{len(races.index)}')

races['Departure Latitude'] = dep_lat
races['Departure Longitude'] = dep_long
races['Arrival Latitude'] = arr_lat
races['Arrival Longitude'] = arr_long
races['Check Distance'] = dist

# sort into race-name order, then add column that gives largest distance in a stage race
races.sort_values(by=['Race'], inplace=True)
b_dist = []
for race in np.arange(len(races.index)-1)+1:
    b_dist.append(dist_calc(radians(dep_lat[len(dep_lat)-1]),
                            radians(dep_long[len(dep_long)-1]),
                            radians(arr_lat[len(arr_lat)-1]),
                            radians(arr_long[len(arr_long)-1])))

        races['Departure Latitude'])

races.to_csv('races_wl.csv')