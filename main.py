import os
import requests
import telegram
import time
import logging

from dotenv import load_dotenv
from tg_handler import TelegramLogsHandler


logger = logging.getLogger()


def main():
    logger.setLevel(logging.INFO)
    
    load_dotenv()

    bot_token = os.environ.get('BOT_TOKEN')
    devman_token = os.environ.get('DEVMAN_TOKEN')

    tg_bot = telegram.Bot(token=bot_token)

    payload = {'Authorization': devman_token}

    user_chat_id = os.environ.get('TG_CHAT_ID')

    tg_handler = TelegramLogsHandler(tg_bot, user_chat_id)

    logger.addHandler(tg_handler)

    fail_connection_count = 0

    desired_timestamp = time.time()

    while True:
        if fail_connection_count == 20:
            time.sleep(600)
            fail_connection_count = 0
        else:
            try:
                payload_params = {'timestamp': desired_timestamp}
                response = requests.get(
                    f'https://dvmn.org/api/long_polling',
                    params=payload_params,
                    headers=payload,
                    timeout=10
                )
                response.raise_for_status()
                check_info = response.json()

                if check_info['status'] == 'found':
                    desired_timestamp = check_info['last_attempt_timestamp']

                    project_title = check_info['new_attempts'][0]['lesson_title']
                    work_status = check_info['new_attempts'][0]['is_negative']

                    if work_status:
                        work_response = 'К сожалению, в работе нашлись ошибки.'
                    else:
                        work_response = 'Преподователю все понравилось, можно приступать к следующему уроку!'

                    tg_bot.send_message(
                        chat_id=user_chat_id,
                        text=f"""У вас проверили работу \"{project_title}\"
{work_response}""",
                        parse_mode=telegram.ParseMode.HTML
                    )

                    logger.info('the message was successfully sent')

                elif check_info['status'] == 'timeout':
                    desired_timestamp = check_info['timestamp_to_request']

            except ConnectionError as connection_e:
                logger.error(connection_e)
                fail_connection_count += 1
            except requests.exceptions.ReadTimeout:
                pass


if __name__ == '__main__':
    main()
