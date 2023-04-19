# Урок 1. Отправляем уведомления о проверке работ
## Чтобы запустить бота, необходимо:

1. Создайте файл .env по следующему примеру:
```
BOT_TOKEN='trj4t4j89r489tj4t4y'
DEVMAN_TOKEN='uyguiog3564654654oihio'
TG_CHAT_ID=123456789
```
2. Устновить зависимости
```shell
pip install -r requirements.txt
```
3. Создайте образ докер контейнера
```shell
docker build -t telegram-bot-1 .
```
4. Запустите докер контейнер
```shell
docker run -d --name telegram-bot-1-container telegram-bot-1
```
