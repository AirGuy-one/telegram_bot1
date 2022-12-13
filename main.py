import os
import requests
import json
import telegram

from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.environ.get('BOT_TOKEN')
DEVMAN_TOKEN = os.environ.get('DEVMAN_TOKEN')

bot = telegram.Bot(token=BOT_TOKEN)

payload = {'Authorization': DEVMAN_TOKEN}

user_chat_id = int(input('Укажите свой chat_id: '))


def main():
    while True:
        try:
            response = requests.get('https://dvmn.org/api/long_polling/', headers=payload, timeout=30)
            if response.status_code:
                response_dict = json.loads(response.text)
                if response_dict['status'] == 'found':
                    print(response_dict)
                    title_of_project = response_dict['new_attempts'][0]['lesson_title']
                    work_status = response_dict['new_attempts'][0]['is_negative']

                    if work_status:
                        work_response = 'К сожалению, в работе нашлись ошибки.'
                    else:
                        work_response = 'Преподователю все понравилось, можно приступать к следующему уроку!'

                    bot.send_message(chat_id=user_chat_id,
                                     text=f"У вас проверили работу \"{title_of_project}\"\n\n"
                                          f"{work_response}",
                                     parse_mode=telegram.ParseMode.HTML)
        except (requests.exceptions.ReadTimeout, ConnectionError) as e:
            print('The interval of 30 seconds has passed...')


if __name__ == '__main__':
    main()



