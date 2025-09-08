from urllib.request import urlopen
import json
import pprint
import random
response = urlopen('https://api.openf1.org/v1/drivers')
data = json.loads(response.read().decode('utf-8'))

randomInt = random.randint(0,len(data))

pprint.pprint(data[randomInt])

