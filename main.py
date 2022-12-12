import requests

DEVMAN_TOKEN='Token d93df5c85681512862e57e04228d6fcf080df87e'

payload = {'Authorization': DEVMAN_TOKEN}

while True:
    try:
        response = requests.get('https://dvmn.org/api/long_polling/', headers=payload, timeout=5)
    except (requests.exceptions.ReadTimeout, ConnectionError) as e:
        print('The interval of 30 seconds has passed...')


print(response.text)

