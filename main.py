import os
import time

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
    fail_connection_count = 0

    while True:
        """ If the connection with the server is not established after 5 attempts, we will take a break for 10 min """
        if fail_connection_count == 5:
            time.sleep(600)
            fail_connection_count = 0
        else:
            try:
                response = requests.get('https://dvmn.org/api/long_polling/', headers=payload, timeout=30)
                if response.status_code:
                    response_data = json.loads(response.text)
                    if response_data['status'] == 'found':
                        project_title = response_data['new_attempts'][0]['lesson_title']
                        work_status = response_data['new_attempts'][0]['is_negative']

                        if work_status:
                            work_response = 'К сожалению, в работе нашлись ошибки.'
                        else:
                            work_response = 'Преподователю все понравилось, можно приступать к следующему уроку!'

                        bot.send_message(chat_id=user_chat_id,
                                         text=f"""У вас проверили работу \"{project_title}\"
{work_response}""",
                                         parse_mode=telegram.ParseMode.HTML)
                else:
                    fail_connection_count += 1
            except (requests.exceptions.ReadTimeout, ConnectionError) as e:
                pass


if __name__ == '__main__':
    main()



