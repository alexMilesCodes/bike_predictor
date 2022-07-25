import pandas as pd
from requests import get
from datetime import datetime
import pytz


data = pd.read_csv('Book5.csv')

x = []
dt_format = "%d/%m/%Y %H:%M"
for i in data.index:
    dt_str = str(data.loc[i, 'date'])+' '+str(data.loc[i, 'start_time'])
    local_dt = datetime.strptime(dt_str, dt_format)
    tz = pytz.timezone(data.loc[i, 'timezone'])
    dt = tz.localize(local_dt)
    x.append(dt.astimezone(pytz.UTC))

data['start_utc'] = x
data['start_unix'] = ((data['start_utc']-datetime(1970, 1, 1).astimezone(pytz.UTC)).view(int)/1e+9)-3600
data['finish_unix'] = data['start_unix'] + data['finish_time']

weather_dep = []
weather_arr = []
for i in data.index:
    lat = data['dep_lat'][i]
    lon = data['dep_long'][i]
    time = str(int(data['start_unix'][i])+int(0.2*data['finish_time'][i]))
    key = '5ce84b1dcac77029347827d990843b54'
    weather_dep.append(get(f'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={time}'
                           f'&appid={key}&units=metric').text)
    lat = data['arr_lat'][i]
    lon = data['arr_long'][i]
    time = str(int(data['finish_unix'][i])-int(0.15*data['finish_time'][i]))
    weather_arr.append(get(f'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={time}'
                           f'&appid={key}&units=metric').text)

data['weather_dep'] = weather_dep
data['weather_arr'] = weather_arr

data.to_csv('Book5.csv', index=False)
