import requests as rs
import pandas as pd
import math
from datetime import datetime


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


# define a function that takes rider, year (to search from) and the current year (to search to)
# ...and returns a list of eligible races
def get_races(rider, year, current_year):
    # scrape all races into 'races':
    races = []
    excl_ends = ['gc', 'kom', 'points', 'youth']
    while year <= current_year:
        # Scrape each race in that year
        temp = rs.get(f'https://www.procyclingstats.com/rider/{rider}/{year}').text
        temp = temp[temp.find('class="seasonResults"'):temp.find('class="rdrResultsSum')]
        while temp.find('href="race/') > -1:
            race, temp = value_extract(temp, 'href="race/', '"', cut=True)
            if sum([race[len(race)-race[::-1].find('/'):].find(end) > -1 for end in excl_ends]) == 0:
                races.append(f'https://www.procyclingstats.com/race/{race}')
        year += 1

    races = list(set(races))

    return races


# define a function that takes in a list of races
# ...and returns a dataframe of the race's details
def get_race_data(races, show=False):
    done = 0
    date = []
    cat = []
    dist = []
    vert = []
    dep = []
    arr = []
    rank = []
    prof = []
    fin = []
    maps = []
    if type(races) == str:
        races = [races]
    for race in races:
        temp = rs.get(race).text
        date.append(value_extract(temp, 'Date:</div> <div>', '<'))
        # date.append(datetime.strptime(value_extract(temp, 'Date:</div> <div>', '<'), '%d %B %Y'))
        cat.append(value_extract(temp, 'Race category:</div> <div>', '<'))
        dist.append(value_extract(temp, 'Distance: </div> <div>', ' km<'))
        vert.append(value_extract(temp, 'Vert. meters:</div> <div>', '<'))
        dep.append(value_extract(temp, 'Departure:</div> <div><a    href="location/', '">'))
        arr.append(value_extract(temp, 'Arrival:</div> <div><a    href="location/', '">'))
        rank.append(value_extract(temp, 'Race ranking:</div> <div>', '<'))
        # *** TYPE OF VALUES MUST BE CHANGED BEFORE MODELLING OBVIOUSLY ***
        temp = rs.get(f'{race}/today/profiles').text
        if value_extract(temp, 'Profile</div><div><img src="', '"'):
            prof.append('https://www.procyclingstats.com/'+value_extract(temp, 'Profile</div><div><img src="', '"'))
        else:
            prof.append('')
        if value_extract(temp, 'Finish profile</div><div><img src="', '"'):
            fin.append('https://www.procyclingstats.com/'+value_extract(temp,
                                                                        'Finish profile</div><div><img src="', '"'))
        else:
            fin.append('')
        maps.append(value_extract(temp, 'Map</div><div><img src="', '"'))

        new = math.floor(((races.index(race))/len(races))*5)
        if done != new:
            done = new
            if show:
                print(f'{int(done*20)}%')

    races_df = pd.DataFrame({'Race': races})
    races_df['Date'] = date
    races_df['Category'] = cat
    races_df['Distance'] = dist
    races_df['Vertical Meters'] = vert
    races_df['Departure Location'] = dep
    races_df['Arrival Location'] = arr
    races_df['Rank'] = rank
    races_df['Profile'] = prof
    races_df['Finish Profile'] = fin
    races_df['Map'] = maps

    return races_df


# define a function that takes in a list of races
# ...and returns a dict of the race's details
def get_race_data_dict(race, show=False):
    temp = rs.get(race).text
    races_dict = {}
    races_dict['Race'] = race
    races_dict['Date'] = value_extract(temp, 'Date:</div> <div>', '<')
    races_dict['Category'] = value_extract(temp, 'Race category:</div> <div>', '<')
    races_dict['Distance'] = value_extract(temp, 'Distance: </div> <div>', ' km<')
    races_dict['Vertical Meters'] = value_extract(temp, 'Vert. meters:</div> <div>', '<')
    races_dict['Departure Location'] = value_extract(temp, 'Departure:</div> <div><a    href="location/', '">')
    races_dict['Arrival Location'] = value_extract(temp, 'Arrival:</div> <div><a    href="location/', '">')
    races_dict['Rank'] = value_extract(temp, 'Race ranking:</div> <div>', '<')
    temp = rs.get(f'{race}/today/profiles').text
    if value_extract(temp, 'Profile</div><div><img src="', '"'):
        prof = 'https://www.procyclingstats.com/'+value_extract(temp, 'Profile</div><div><img src="', '"')
    else:
        prof = ''
    if value_extract(temp, 'Finish profile</div><div><img src="', '"'):
        fin = 'https://www.procyclingstats.com/'+value_extract(temp, 'Finish profile</div><div><img src="', '"')
    else:
        fin = ''
    maps = value_extract(temp, 'Map</div><div><img src="', '"')
    races_dict['Profile'] = prof
    races_dict['Finish Profile'] = fin
    races_dict['Map'] = maps

    return races_dict


# define a function that takes in:
#    df - a dataframe of race details
#    rider - the name of the rider
#    rivals - a list of key rivals
#    teammates - a list of teammates
# ...and returns df containing the results
def get_race_results(df, rider,  rivals, teammates, include_dns=False, show=False):
    data = {'Place': [], 'Num Places': [], 'Num Places Finishers': [], 'Tag': [], 'Team': []}
    for name in (rivals+teammates):
        data[name] = []
    done = 0
    for race in df['Race']:
        temp = rs.get(race).text
        names = []
        tags = []
        teams = []
        while temp.find('href="rider/') > -1:
            temp2 = temp[:temp.find('href="rider/')]
            temp = temp[temp.find('href="rider/')+12:]
            if (len(names) == 0 or temp2.find('<td>DNS</td>') == -1) and names.count(temp[:temp.find('"')]) == 0:
                names.append(temp[:temp.find('"')])
                teams.append(value_extract(temp, 'href="team/', '"'))
                if temp2.find('<td>DNF</td>') > -1:
                    tags.append('DNF')
                elif temp2.find('<td>OTL</td>') > -1:
                    tags.append('OTL')
                else:
                    tags.append('')
        # if rider's name is missing, that means he is DNS, so add as Place: -1, Tag: 'DNS'
        if names.count(rider) <= 0:
            data['Place'].append(-1)
            data['Tag'].append('DNS')
            data['Team'].append('')
        else:
            data['Place'].append(names.index(rider)+1)
            data['Tag'].append(tags[names.index(rider)])
            data['Team'].append(teams[names.index(rider)])
        data['Num Places'].append(len(names))
        data['Num Places Finishers'].append(tags.count(''))
        # logic to check whether rivals were rivals and teammates were teammates
        for name in rivals:
            data[name].append(False)
            if names.count(name) > 0 and names.count(rider) > 0:
                if teams[names.index(name)] != teams[names.index(rider)]:
                    data[name][len(data[name])-1] = True
        for name in teammates:
            data[name].append(False)
            if names.count(name) > 0 and names.count(rider) > 0:
                if teams[names.index(name)] == teams[names.index(rider)]:
                    data[name][len(data[name])-1] = True

        new = math.floor(((list(df['Race']).index(race))/len(df['Race']))*5)
        if done != new:
            done = new
            if show:
                print(f'{done*20}%')

    for col in list(data.keys()):
        df[col] = data[col]
    if not include_dns:
        df = df[df['Tag'] != 'DNS']
    return df


# define a function that takes in a list of races
# ...and returns a dictionary with the race profiles and distances
def get_race_profile(race):
    temp = value_extract(rs.get(f'{race}/today/profiles').text, 'Profile</div><div ><img src="', '"')
    if temp:
        prof = 'https://www.procyclingstats.com/'+temp
    else:
        prof = ''
    dist = value_extract(rs.get(race).text, 'Distance: </div> <div>', ' km<')

    return {'Race': race, 'Distance': dist, 'Profile': prof}
