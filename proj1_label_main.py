import scrapers
import labelling
import requests as rs
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


old = pd.read_csv('profiles.csv')
na_old = pd.read_csv('na_profiles.csv')

# input rider name and check if the site for this rider exists
current_year = datetime.now().year
rider = input('enter a rider whose results are scraped: ')
while rs.get(f'https://www.procyclingstats.com/rider/{rider}').text.find('Date of birth:</b> 0<sup>th') != -1:
    print(f'can\'t find a rider named "{rider}"')
    print('input format: [forename]-[forename]-...-[surname]')
    rider = input('enter a rider whose results are scraped: ')

# input the starting year of the scrape
year = input('enter starting year of scrape (leave blank for 1990): ')
if not year.isdigit():
    if year:
        print('not recognised - starting year set to 1990')
    year = 1990
elif not (1900 <= int(year) <= current_year):
    print('out of range - starting year set to 1990')
    year = 1990
year = int(year)

print(f'searching races from {year} to {current_year} ...')

races = scrapers.get_races(rider, year, current_year)

print(f'{len(races)} races found')

count_excl = 0
for race in races:
    if ''.join(list(old['Race'].astype('string'))).find(str(race)) > -1:
        races.remove(race)
        count_excl += 1
print(f'{count_excl} races already labelled')

count_excl = 0
for race in races:
    if ''.join(list(na_old['Race'].astype('string'))).find(str(race)) > -1:
        races.remove(race)
        count_excl += 1
print(f'{count_excl} races deemed not applicable')

# initialise global mouse coordinates
x = 0
y = 0

# initialise lists to fill what will go in the profile table
names = []
distance = []
cobbles = []
profiles = []
race_name = []
wt = []
notes = []
na = []
for i in range(1650):
    profiles.append([])

labelled = 0
exi = False
change = False
for race in range(len(races)):
    if not exi:
        df = scrapers.get_race_profile(races[race])
        if df['Profile']\
           and ''.join(list(old['Link'].astype('string'))).find(str(df['Profile'])) == -1\
           and ''.join(list(old['Race'].astype('string'))).find(str(df['Race'])) == -1:
            print(df['Profile'])
            # match = True false flag as to whether or not it is mostly white and green
            # if match is false: cont == 0
            cont = input('is this profile suitable for labelling? (enter 0 to skip,'
                         ' 1 to continue and tag as cobbled'
                         ', 9 to exit the program): ')
            if cont == '9':
                exi = True
                cont = '0'
            if cont != '0':
                try:
                    float(df['Distance'])
                except ValueError:
                    print('not a valid distance')
                    cont = '0'
            if cont != '0':
                if cont == '1':
                    cobbles.append(1)
                else:
                    cobbles.append(0)
                print(df['Race'])
                in_wt = input('enter 0 if not in world tour: ')
                if in_wt != '0':
                    in_wt = 1
                wt.append(in_wt)
                alt = labelling.label_profile(df['Profile'])
                dis = float(df['Distance'])
                # spike removal
                # for i in range(len(alt)-1):
                #     if abs(len(alt)*(alt[i+1]-alt[i])/dis) > 300:
                #         alt[i+1] = (alt[i]+alt[i+2])/2
                distance.append(dis)
                race_name.append(df['Race'])
                names.append(df['Profile'])
                alt_x = np.zeros(len(alt))
                for i in range(len(alt)):
                    alt_x[i] = (i+1)*dis/len(alt_x)
                    profiles[i].append(alt[i])
                for i in range(len(alt), 1650):
                    profiles[i].append('')
                plt.plot(alt_x, alt)
                plt.title('exit this window to continue')
                plt.show()
                notes.append(input('enter notes to add for profile (type "delete" to remove): '))
                if notes[len(notes)-1] != 'delete':
                    labelled += 1
                change = True
            else:
                na.append(df['Race'])
        if not exi and change:
            print(f'{labelled} profiles labelled this session')
            change = False

print('exiting: compiling data...')

new = pd.DataFrame({'Link': names})
new['Race'] = race_name
new['Distance'] = distance
new['Cobbled?'] = cobbles
new['WT?'] = wt
new['Note'] = notes
for i in range(1650):
    new[str(i)] = profiles[i]

input('have you closed profiles.csv?')

new = new[new['Note'] != 'delete']
new = pd.concat([old, new])
na_new = pd.DataFrame({'Race': na})
na_new = pd.concat([na_old, na_new])

print('exiting: uploading to files...')

new.to_csv('profiles.csv', index=False)
na_new.to_csv('na_profiles.csv', index=False)

print('done')
