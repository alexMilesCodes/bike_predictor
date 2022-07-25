import pandas as pd
from math import sin, cos, sqrt, atan2, radians, pi, degrees


# function to calculate km between locations
def dist_calc(lat1, lon1, lat2, lon2, r=6373.0):

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return r * c


# function to calculate angle between locations and north
def azimuth_calc(lat1, lon1, lat2, lon2):

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1

    return degrees(pi+atan2(sin(dlon)*cos(lat2), cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(dlon)))


data = pd.read_csv('/Users/alexmiles/PycharmProjects/bike_team_maker/Book3.csv')

coord_dist = []
angle = []
for i in data.index:
    coord_dist.append(dist_calc(data['arr_lat'][i], data['arr_long'][i], data['dep_lat'][i], data['dep_long'][i]))
    angle.append(azimuth_calc(data['arr_lat'][i], data['arr_long'][i], data['dep_lat'][i], data['dep_long'][i]))

data['coord_dist'] = coord_dist
data['angle'] = angle

data.to_csv('/Users/alexmiles/PycharmProjects/bike_team_maker/Book3.csv', index=False)
