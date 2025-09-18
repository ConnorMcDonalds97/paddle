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

    