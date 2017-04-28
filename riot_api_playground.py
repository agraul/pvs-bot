import requests
from id import riotkey

# pulling all champions
developer_key = riotkey()
champions = requests.get('https://euw1.api.riotgames.com/lol/platform/v3/champions?api_key={}'.format(developer_key))
#print(champions.json())

payload = {'api_key': developer_key}
champs = requests.get('https://euw1.api.riotgames.com/lol/platform/v3/champions', params=payload)
print(champs.url)
