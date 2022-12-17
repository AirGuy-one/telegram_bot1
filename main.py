import os
import requests
import json
import telegram
import time

from datetime import datetime
from dotenv import load_dotenv


def main():
    load_dotenv()

    bot_token = os.environ.get('BOT_TOKEN')
    devman_token = os.environ.get('DEVMAN_TOKEN')

    bot = telegram.Bot(token=bot_token)

    payload = {'Authorization': devman_token}

    user_chat_id = os.environ.get('CHAT_ID')

    fail_connection_count = 0
    response_number = 0
    desired_timestamp = 0

    while True:
        """ If server dont answer after 20 attempts, we will take a break for 10 minutes """
        if fail_connection_count == 20:
            time.sleep(600)
            fail_connection_count = 0
        else:
            try:
                # Here we get the count of seconds that have passed since 1970
                current_time = int((datetime.now() - datetime(1970, 1, 1)).total_seconds())
                if response_number == 0:
                    desired_timestamp = current_time - 300
                response = requests.get(
                    # First time we subtract 5 minutes from the current time
                    # Later we use the timestamp from the server response
                    f'https://dvmn.org/api/long_polling/?timestamp={desired_timestamp}',
                    headers=payload,
                    timeout=10
                )
                response.raise_for_status()
                check_info = json.loads(response.text)

                desired_timestamp = check_info['request_query'][0][1]

                if check_info['status'] == 'found':
                    project_title = check_info['new_attempts'][0]['lesson_title']
                    work_status = check_info['new_attempts'][0]['is_negative']

                    if work_status:
                        work_response = 'К сожалению, в работе нашлись ошибки.'
                    else:
                        work_response = 'Преподователю все понравилось, можно приступать к следующему уроку!'

                    bot.send_message(
                        chat_id=user_chat_id,
                        text=f"""У вас проверили работу \"{project_title}\"
{work_response}""",
                        parse_mode=telegram.ParseMode.HTML
                    )
                response_number += 1
            except ConnectionError:
                fail_connection_count += 1
            except requests.exceptions.ReadTimeout:
                pass


if __name__ == '__main__':
    main()
