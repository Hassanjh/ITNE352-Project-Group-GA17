import json
from pip._vendor import requests

params= {
    'access_key':'2959aad3afc26c5f3c550ef7640cf3b6',
    'arr_icao': 'OBBI',
    'limit': 100
}

api_response = requests.get('http://api.aviationstack.com/v1/flights',params)
json_result = api_response.json()


with open ('GA17.json','w') as j:
    json.dump(json_result,j, indent=2)