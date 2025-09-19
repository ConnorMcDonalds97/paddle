function similar(a, b) {
    // Function to check for string similarity
    if (!a || !b) return 0;
    a = a.toLowerCase();
    b = b.toLowerCase();
    let matches = 0;
    for (let i = 0; i < Math.min(a.length, b.length); i++) {
        if (a[i] === b[i]) matches++;
    }
    return matches / Math.max(a.length, b.length);
}

function printDriverInfo(driverDict) {
    console.log('Driver name: ' + driverDict["full_name"]);
    console.log('Driver team: ' + driverDict['team_name']);
    console.log('Team Color: ' + driverDict['team_colour'] + '\n');
}

function checkWin(selectedDriver, guessedDriver, constructorStandings){
    let nameCorrect = false;
    let teamCorrect = false;
    let colourCorrect = false;

    let result = ''

    if (selectedDriver.full_name === guessedDriver.full_name) {
        nameCorrect = true
        result += 'Name: Correct'
    } else {
        result += 'Name: Incorrect'
    }

    if (selectedDriver.team_name === guessedDriver.team_name) {
        teamCorrect = true;
        result += 'Team: Correct'
    } else {
        const teamResult = checkTeam(selectedDriver, guessedDriver, constructorStandings);
        if (teamResult === 0) {
            result += 'Team: Incorrect | ^'
        } else {
            result += 'Team: Incorrect | v'
        }
    }

    if (selectedDriver.team_colour === guessedDriver.team_colour) {
        colourCorrect = true;
        result += 'Colour: correct'
    } else {
        result += 'Colour: Incorrect'
    }

    return nameCorrect && teamCorrect && colourCorrect ? 1 : 0;
}

function checkTeam(selectedDriver, guessedDriver, standings) {
    /*
    Returns 0 if correct team is better, 1 if the correct team is worse
    */
    const correctTeam = selectedDriver.team_name;
    const guessedTeam = guessedDriver.team_name;
    const correctTeamRank = parseInt(standings[correctTeam][0]);
    const guessedTeamRank = parseInt(standings[guessedTeam][0]);

    // console.log('correct team: ', correctTeamRank);
    // console.log('guessed team: ', guessedTeamRank);

    if (correctTeamRank > guessedTeamRank) {
        return 1;
    } else {
        return 0;
    }
}

function mapConstructorNames(constructorStandings, driverData) {
    // Build a mapping from lowercase constructorId to team_name from driver info
    const teamMap = {};
    for (const driver of driverData) {
        const teamName = driver.team_name;
        if (teamName) {
            const key = teamName.trim().toLowerCase().replace(/ /g, "_").replace(/-/g, "_");
            teamMap[key] = teamName;
        }
    }

    // Special cases for known mismatches
    teamMap["rb"] = "Racing Bulls";
    teamMap["sauber"] = "Kick Sauber";
    teamMap["alfa_romeo"] = "Alfa Romeo";
    teamMap["haas"] = "Haas F1 Team";
    teamMap["alphatauri"] = "AlphaTauri";
    teamMap['red_bull'] = 'Red Bull Racing';

    const newStandings = {};
    for (const [constructorId, value] of Object.entries(constructorStandings)) {
        // Try to find the matching team name
        const teamName = teamMap[constructorId] || constructorId;
        newStandings[teamName] = value;
    }
    return newStandings;
}

// Main game logic
let driverData = [];
let constructorStandingsDict = {};
let selectedDriver = null;
let win = false;

async function fetchData() {
    // Fetch driver info
    const driverRes = await fetch('https://api.openf1.org/v1/drivers?session_key=latest');
    driverData = await driverRes.json();

    // Fetch constructor standings
    const standingsRes = await fetch('https://api.jolpi.ca/ergast/f1/2025/constructorstandings');
    const standingsData = await standingsRes.json();
    const constructorStandings = standingsData.MRData.StandingsTable.StandingsLists[0].ConstructorStandings;
    constructorStandingsDict = {};
    for (const constructor of constructorStandings) {
        constructorStandingsDict[constructor.Constructor.constructorId] = [constructor.position, constructor.points];
    }
    constructorStandingsDict = mapConstructorNames(constructorStandingsDict, driverData);
}

function startGame() {
    win = false;
    // Randomly select a driver
    const randomInt = Math.floor(Math.random() * driverData.length);
    selectedDriver = driverData[randomInt];
    printDriverInfo(selectedDriver);
    document.getElementById('result').innerHTML = '';
}

function renderResultSquares(selectedDriver, guessedDriver, constructorStandings) {
    const squaresContainer = document.getElementById('result-squares');

    // Create a row container for this guess
    const row = document.createElement('div');
    row.style.display = 'flex';
    row.style.alignItems = 'center';
    row.style.marginBottom = '8px';

    // Optionally show guessed driver name
    const nameLabel = document.createElement('span');
    nameLabel.textContent = guessedDriver.full_name;
    nameLabel.style.marginRight = '12px';
    nameLabel.style.color = '#fff';
    nameLabel.style.fontSize = '18px';
    row.appendChild(nameLabel);

    // Team
    let teamClass = 'incorrect';
    let arrowType = null; // 'up' or 'down'
    if (selectedDriver.team_name === guessedDriver.team_name) {
        teamClass = 'correct';
    } else {
        const teamResult = checkTeam(selectedDriver, guessedDriver, constructorStandings);
        if (teamResult === 0) {
            arrowType = 'up';
        } else {
            arrowType = 'down';
        }
    }
    const teamSquare = document.createElement('div');
    teamSquare.className = `result-square ${teamClass}`;
    // Label
    const teamLabel = document.createElement('span');
    teamLabel.textContent = 'Team';
    teamLabel.style.display = 'inline-block';
    teamLabel.style.marginRight = arrowType ? '8px' : '0';
    teamSquare.appendChild(teamLabel);
    // Arrow
    if (arrowType) {
        const arrow = document.createElement('span');
        arrow.className = `result-arrow ${arrowType}`;
        arrow.textContent = arrowType === 'up' ? '↑' : '↓';
        teamSquare.appendChild(arrow);
    }
    row.appendChild(teamSquare);

    // Colour
    let colourClass = 'incorrect';
    if (selectedDriver.team_colour === guessedDriver.team_colour) {
        colourClass = 'correct';
    }
    const colourSquare = document.createElement('div');
    colourSquare.className = `result-square ${colourClass}`;
    colourSquare.textContent = 'Colour';
    row.appendChild(colourSquare);

    // Append this row to the container (history)
    squaresContainer.appendChild(row);
}

// Update handleGuess to call renderResultSquares
function handleGuess() {
    if (win) return;
    const userGuess = document.getElementById('guess-input').value.trim().toLowerCase();
    let found = false;
    let bestMatch = null;
    let bestScore = 0;
    for (const driver of driverData) {
        const score = similar(userGuess, driver.full_name.toLowerCase());
        if (score > bestScore) {
            bestScore = score;
            bestMatch = driver;
        }
    }
    // Accept the best match if similarity is above a reasonable threshold (e.g., 0.6)
    if (bestMatch && bestScore > 0.6) {
        win = checkWin(selectedDriver, bestMatch, constructorStandingsDict);
        document.getElementById('result').innerHTML = win ? 'You win!' : 'Try again!';
        renderResultSquares(selectedDriver, bestMatch, constructorStandingsDict);
        found = true;
    }
    if (!found) {
        document.getElementById('result').innerHTML = 'No matching driver found.';
        document.getElementById('result-squares').innerHTML = '';
    }
}

window.onload = async function() {
    await fetchData();
    startGame();
    document.getElementById('guess-btn').onclick = handleGuess;
    document.getElementById('guess-input').addEventListener('keydown', function(e) {
        if (e.key === 'Enter') handleGuess();
    });
};


