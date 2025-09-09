from urllib.request import urlopen
from difflib import SequenceMatcher
import json
import pprint
import random
'''
API's used:
1. openF1 for driver info
2. jolpica-f1 for driver standings
'''

def printDriverInfo(driverDict):
    print('Driver name: ' + driverDict["full_name"])
    print('Driver team: ' + driverDict['team_name'])
    print('Team Color: ' + driverDict['team_colour'] + '\n')



response = urlopen('https://api.openf1.org/v1/drivers')
data = json.loads(response.read().decode('utf-8'))

randomInt = random.randint(0,len(data))

selectedDriver = data[randomInt]

printDriverInfo(selectedDriver)

standingsApiCall = urlopen('https://api.jolpi.ca/ergast/f1/2025/constructorstandings')

standingsData = json.loads(standingsApiCall.read().decode('utf-8'))

constructorStandings = standingsData["MRData"]["StandingsTable"]["StandingsLists"][0]["ConstructorStandings"]

constructorStandingsDict = {}
'''
This dictionary is of the format:
{
    'team_name': [position,points],
    'team_name': [position,points],
    .
    .
    .
}
'''

# pprint.pprint(driverStandings)
for constructor in constructorStandings:
    constructorStandingsDict[constructor["Constructor"]["constructorId"]] = [constructor["position"],constructor["points"] ]

pprint.pprint(constructorStandingsDict)

# print(selectedDriver['full_name'])

# userGuess = input('guess the driver: ')

# def similar(a,b):
#     return SequenceMatcher(None, a, b).ratio()

# gameWin = False

# while (not gameWin):
#     userGuess = input('guess the driver: ')

#     if (similar(userGuess.lower() ,selectedDriver['full_name'].lower())) > 0.7:
#         print('yay!')
#         gameWin = True
#     else:
#         print('uh oh')
#         print(selectedDriver['team_colour'])
#         print(selectedDriver['team_name'])

