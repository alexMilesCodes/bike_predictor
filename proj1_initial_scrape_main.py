import scrapers
import requests as rs
from datetime import datetime


# input rider name and check if the site for this rider exists
current_year = datetime.now().year
rider = input('enter a rider whose results are scraped: ')
while rs.get(f'https://www.procyclingstats.com/rider/{rider}').text.find('Page not found') > -1:
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

rivals = []
rival = 'temp'
while rival:
    rival = input('enter a rival (leave blank to continue): ')
    if rival:
        while rs.get(f'https://www.procyclingstats.com/rider/{rival}').text.find('Page not found') > -1:
            print(f'can\'t find a rider named "{rival}"')
            print('input format: [forename]-[forename]-...-[surname]')
            rival = input('enter a rival (leave blank to continue): ')
        if rival:
            if rivals.count(rival) == 0:
                print(f'{rival} added')
                rivals.append(rival)
            else:
                print('already added')

teammates = []
teammate = 'temp'
while teammate:
    teammate = input('enter a teammate (leave blank to continue): ')
    if teammate:
        while rs.get(f'https://www.procyclingstats.com/rider/{teammate}').text.find('Page not found') > -1:
            print(f'can\'t find a rider named "{teammate}"')
            print('input format: [forename]-[forename]-...-[surname]')
            teammate = input('enter a teammate (leave blank to continue): ')
        if teammate:
            if teammates.count(teammate) == 0:
                print(f'{teammate} added')
                teammates.append(teammate)
            else:
                print('already added')

print(f'searching races from {year} to {current_year} ...')

races = scrapers.get_races(rider, year, current_year)

print(f'{len(races)} races found')
print('scraping race details ...')

races_df = scrapers.get_race_data(races, show=True)

print('done')

print('scraping race results ...')

races_df = scrapers.get_race_results(races_df, rider, rivals, teammates, show=True)

print('done')

f = open("races.csv", "w")
f.truncate()
f.close()

races_df.to_csv('races.csv')
