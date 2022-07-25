import pandas as pd
from timezonefinder import TimezoneFinder


tf = TimezoneFinder()
tz = tf.timezone_at(lng=13.358, lat=52.5061)

data = pd.read_csv('basefile-3.csv').convert_dtypes()

dep_zone = []
arr_zone = []
for i in data.index:
    dep_zone.append(tf.timezone_at(lng=data.loc[i, 'dep_long'], lat=data.loc[i, 'dep_lat']))
    arr_zone.append(tf.timezone_at(lng=data.loc[i, 'arr_long'], lat=data.loc[i, 'arr_lat']))

data['dep_zone'] = dep_zone
data['arr_zone'] = arr_zone

data.to_csv('basefile-4.csv', index=False)

temp = []
wind = []
prec = []
humid = []
cloud = []
