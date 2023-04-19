# Урок 1. Отправляем уведомления о проверке работ
## Чтобы запустить бота через docker контейнер, необходимо:

1. Создайте файл .env по следующему примеру:
```
BOT_TOKEN='trj4t4j89r489tj4t4y'
DEVMAN_TOKEN='uyguiog3564654654oihio'
TG_CHAT_ID=123456789
```
2. Создайте образ докер контейнера
```shell
docker build -t telegram-bot-1 .
```
3. Запустите докер контейнер
```shell
docker run -d --name telegram-bot-1-container telegram-bot-1
```

## Чтобы запустить бота локально, необходимо:

1. Создайте файл .env по следующему примеру:
```
BOT_TOKEN='trj4t4j89r489tj4t4y'
DEVMAN_TOKEN='uyguiog3564654654oihio'
TG_CHAT_ID=123456789
```
2. Создайте образ докер контейнера
```shell
pip install -r requirements.txt
```
3. Запустите бота
```shell
python3 main.py
```


