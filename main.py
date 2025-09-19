from urllib.request import urlopen
import json
import pprint
import random

# from functions import similar
# from functions import checkWin
# from functions import printDriverInfo
# from functions import checkTeam
# from functions import map_constructor_names
'''
API's used:
1. openF1 for driver info
2. jolpica-f1 for driver standings
'''

from difflib import SequenceMatcher

def similar(a,b):
    return SequenceMatcher(None, a, b).ratio()

def printDriverInfo(driverDict):
    print('Driver name: ' + driverDict["full_name"])
    print('Driver team: ' + driverDict['team_name'])
    print('Team Color: ' + driverDict['team_colour'] + '\n')

def checkWin (selectedDriver, guessedDriver, constructorStandings):
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
        result = checkTeam(selectedDriver, guessedDriver, constructorStandings)
        if result == 0:
            print('Team: Incorrect | ^')
        else:
            print('Team: Incorrect | v')

    if selectedDriver['team_colour'] == guessedDriver['team_colour']:
        colourCorrect = True
        print('Colour: Correct')
    else:
        print('Colour: Incorrect')

    if nameCorrect and teamCorrect and colourCorrect:
        return 1
    else:
        return 0

def checkTeam(selectedDriver, guessedDriver, standings):
    '''
    Returns 0 if correct team is better, 1 if the correct team is worse
    '''
    correctTeam = selectedDriver['team_name']
    guessedTeam = guessedDriver['team_name']
    correctTeamRank = int(standings[correctTeam][0])
    guessedTeamRank = int(standings[guessedTeam][0])

    #print('correct team: ', correctTeamRank)
    #print('guessed team: ', guessedTeamRank)


    if correctTeamRank > guessedTeamRank:
        return 1
    else:
        return 0

def map_constructor_names(constructor_standings, driver_data):
    # Build a mapping from lowercase constructorId to team_name from driver info
    team_map = {}
    for driver in driver_data:
        team_name = driver.get("team_name")
        if team_name:
            key = team_name.strip().lower().replace(" ", "_").replace("-", "_")
            team_map[key] = team_name

    # Special cases for known mismatches
    team_map["rb"] = "Racing Bulls"
    team_map["sauber"] = "Kick Sauber"
    team_map["alfa_romeo"] = "Alfa Romeo"
    team_map["haas"] = "Haas F1 Team"
    team_map["alphatauri"] = "AlphaTauri"
    team_map['red_bull'] = 'Red Bull Racing'

    new_standings = {}
    for constructor_id, value in constructor_standings.items():
        # Try to find the matching team name
        team_name = team_map.get(constructor_id, constructor_id)
        new_standings[team_name] = value
    return new_standings

    


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