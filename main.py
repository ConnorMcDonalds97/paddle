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
def similar(a,b):
    return SequenceMatcher(None, a, b).ratio()

def printDriverInfo(driverDict):
    print('Driver name: ' + driverDict["full_name"])
    print('Driver team: ' + driverDict['team_name'])
    print('Team Color: ' + driverDict['team_colour'] + '\n')

def checkWin (selectedDriver, guessedDriver):
    nameCorrect = False
    teamCorrect = False
    colourCorrect = False

    if selectedDriver['full_name'] == guessedDriver['full_name']:
        nameCorrect = True
        print('Name: Correct')
    else:
        print('Name: Incorrect')
    
    if selectedDriver['team_name'] == guessedDriver['team_name']:
        teamCorrect = True
        print('Team: Correct')
    else:
        print('Team: Incorrect')

    if selectedDriver['team_colour'] == guessedDriver['team_colour']:
        colourCorrect = True
        print('Colour: Correct')
    else:
        print('Colour: Incorrect')

def main():
    response = urlopen('https://api.openf1.org/v1/drivers?session_key=latest')
    driverData = json.loads(response.read().decode('utf-8'))

    # for driver in driverData:
    #     driver["full_name"] = driver["full_name"].lower()

    # pprint.pprint(driverData)

    randomInt = random.randint(0,len(driverData))

    selectedDriver = driverData[randomInt]

    printDriverInfo(selectedDriver)

    ####################################################################################

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

    print(selectedDriver['full_name'])

    userGuess = input('guess the driver: ')

    print('\nguess: ', userGuess.strip().lower())

    guessedDriver = 0
    lowercaseGuess = userGuess.lower()


    for drivers in driverData:

        if (similar(lowercaseGuess, drivers['full_name'].lower()) > 0.9):

            checkWin(selectedDriver,drivers)

            break

if __name__ == '__main__':
    main()
