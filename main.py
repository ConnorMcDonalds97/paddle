from urllib.request import urlopen
from difflib import SequenceMatcher
import json
import pprint
import random



response = urlopen('https://api.openf1.org/v1/drivers')
data = json.loads(response.read().decode('utf-8'))

randomInt = random.randint(0,len(data))

selectedDriver = data[randomInt]

pprint.pprint(selectedDriver)

print(selectedDriver['full_name'])

userGuess = input('guess the driver: ')

def similar(a,b):
    return SequenceMatcher(None, a, b).ratio()

if (similar(userGuess.lower() ,selectedDriver['full_name'].lower())) > 0.7:
    print('yay!')