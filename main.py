import requests
import telegram

DEVMAN_TOKEN='Token d93df5c85681512862e57e04228d6fcf080df87e'
BOT_TOKEN='5908796517:AAGXALrwq_Y2uYH8_4yp1wnhdIZohKC_TME'

bot = telegram.Bot(token=BOT_TOKEN)

payload = {'Authorization': DEVMAN_TOKEN}

# while True:
#     try:
#         response = requests.get('https://dvmn.org/api/long_polling/', headers=payload, timeout=5)
#     except (requests.exceptions.ReadTimeout, ConnectionError) as e:
#         print('The interval of 30 seconds has passed...')

user_chat_id = 746935610

name = 'Billy'

bot.send_message(chat_id=user_chat_id,
                text=f"Hello {name}",
                parse_mode=telegram.ParseMode.HTML)

