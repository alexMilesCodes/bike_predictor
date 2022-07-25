import pandas as pd
from datetime import timedelta
from meteostat import Point, Hourly


data = pd.read_csv('basefile-4.csv').convert_dtypes()

data['start_datetime'] = pd.to_datetime(pd.to_datetime(data['date']).astype(int)+(12+(25/60))*60*60000000000)
data['finish_datetime'] = pd.to_datetime(pd.to_datetime(data['date']).astype(int)+(12+(25/60))*60*60000000000
                                                                                 + 1000000000*data['finish_time'])


i = data.index[0]
wthr = Hourly(Point(data.loc[i, 'arr_lat'], data.loc[i, 'arr_long'], data.loc[i, 'arr_alt']),
              start=data.loc[i, 'start_datetime']-timedelta(hours=1), end=data.loc[i, 'start_datetime'],
              timezone=data.loc[i, 'arr_zone']
              ).fetch()
wthr['Race'] = [data.loc[i, 'Race']]
for i in data.index[1:]:
    temp = Hourly(Point(data.loc[i, 'arr_lat'], data.loc[i, 'arr_long'], data.loc[i, 'arr_alt']),
                  start=data.loc[i, 'start_datetime']-timedelta(hours=1), end=data.loc[i, 'start_datetime'],
                  timezone=data.loc[i, 'arr_zone']
                  ).fetch()
    if not temp.empty:
        temp['Race'] = [data.loc[i, 'Race']]
        wthr = wthr.append(temp, ignore_index=True)
    print(i)

wthr.to_csv('weather-arr.csv', index=False)
