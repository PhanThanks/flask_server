import requests

BOT_TOKEN = '7699455070:AAEb0lEsOrQq9pnL_r3wEgDbqpXWk-mrwU0'
CHAT_ID = '7428847722'

def send_telegram(image_path, caption='Phát hiện người!'):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(image_path, 'rb') as img:
        files = {'photo': img}
        data = {'chat_id': CHAT_ID, 'caption': caption}
        requests.post(url, files=files, data=data)
