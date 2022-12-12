import requests

DEVMAN_TOKEN='Token d93df5c85681512862e57e04228d6fcf080df87e'

response = requests.get('https://dvmn.org/api/long_polling/', headers={'Authorization': DEVMAN_TOKEN})

print(response.text)

