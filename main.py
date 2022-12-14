import os
import requests
import json
import telegram
import time

from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.environ.get('BOT_TOKEN')
DEVMAN_TOKEN = os.environ.get('DEVMAN_TOKEN')

bot = telegram.Bot(token=BOT_TOKEN)

payload = {'Authorization': DEVMAN_TOKEN}

user_chat_id = os.environ.get('CHAT_ID')


def main():
    fail_connection_count = 0

    while True:
        """ If server dont answer after 20 attempts, we will take a break for 10 minutes """
        if fail_connection_count == 20:
            time.sleep(600)
            fail_connection_count = 0
        else:
            try:
                response = requests.get('https://dvmn.org/api/long_polling/?timestamp=10000000000',
                                        headers=payload,
                                        timeout=10)
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
                fail_connection_count += 1


if __name__ == '__main__':
    main()



