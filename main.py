from urllib.request import urlopen
import json
import pprint
import random

from functions import similar
from functions import checkWin
from functions import printDriverInfo
from functions import checkTeam
from functions import map_constructor_names
'''
API's used:
1. openF1 for driver info
2. jolpica-f1 for driver standings
'''


def main():
    response = urlopen('https://api.openf1.org/v1/drivers?session_key=latest')
    driverData = json.loads(response.read().decode('utf-8'))

    # for driver in driverData:
    #     driver["full_name"] = driver["full_name"].lower()

    # pprint.pprint(driverData)

    randomInt = random.randint(0,len(driverData)-1)

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

    constructorStandingsDict = map_constructor_names(constructorStandingsDict, driverData)

    #pprint.pprint(constructorStandingsDict)

    #print(selectedDriver['full_name'])

    
    print("############################################################")
    userGuess = input('guess the driver: ')

    print('\nguess: ', userGuess.strip().lower())

    guessedDriver = 0
    lowercaseGuess = userGuess.lower()


    for drivers in driverData:

        if (similar(lowercaseGuess, drivers['full_name'].lower()) > 0.9):

            win = checkWin(selectedDriver,drivers, constructorStandingsDict)

            break

    while not win:
        print("############################################################")
        userGuess = input('guess the driver: ')

        print('\nguess: ', userGuess.strip().lower())

        guessedDriver = 0
        lowercaseGuess = userGuess.lower()


        for drivers in driverData:

            if (similar(lowercaseGuess, drivers['full_name'].lower()) > 0.9):

                win = checkWin(selectedDriver,drivers, constructorStandingsDict)

                break


if __name__ == '__main__':
    main()