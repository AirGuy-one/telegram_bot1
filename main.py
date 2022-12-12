import requests
import telegram

load_dotenv()


BOT_TOKEN = os.environ.get('BOT_TOKEN')
DEVMAN_TOKEN = os.environ.get('DEVMAN_TOKEN')

bot = telegram.Bot(token=BOT_TOKEN)

payload = {'Authorization': DEVMAN_TOKEN}

user_chat_id = int(input('Укажите свой chat_id: '))

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

