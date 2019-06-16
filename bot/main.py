import requests
import re
from flask import Flask
from flask.views import MethodView
from flask import request
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
TOKEN = os.environ.get('TOKEN')
API_URL = os.environ.get('API_URL')
TELEGRAM_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

def get_data_from_api(command):
    url = API_URL + command
    session = requests.Session()
    r = session.get(url).json()
    return r

def send_message(chat_id, msg):
    session = requests.Session()
    r = session.get(TELEGRAM_URL, params=dict(chat_id=chat_id, 
                                    text=msg, 
                                    parse_mode='Markdown'))
    return r.json()


def parse_text(text_msg):
    '''/start /help, /city /sp, @kiyv @python'''
    addresses = {'city': '/cities', 'sp': '/sp'}
    command_p = r'/\w+'
    message = 'Неверный запрос'
    if '/' in text_msg:
        if '/start' in text_msg or  '/help' in text_msg:
            message = '''Для того, чтобы узнать, какие города доступны, отправьте в сообщении `/city`. 
            Чтобы узнать о доступных специальностях - отправьте `/sp` 
            Чтобы сделать запрос на сохраненные вакансии, отправьте в сообщении через пробел - @город @специальность. 
            Например так - `@kyiv @python`  '''
            return message
        else:
            command = re.search(command_p, text_msg).group().replace('/', '')
            command = addresses.get(command, None)
            return [command] if command else None
        
    else:
        return message

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        resp = request.get_json()
        print(resp)
        return '<h1> Hi Telegram!!! </h1>'
    return '<h1> Hi BOT!!! </h1>'

class BotAPI(MethodView):

    def get(self):
       return '<h1> Hi BOT_Class!!! </h1>'

    def post(self):
        resp = request.get_json()
        text_msg = resp['message']['text']
        chat_id = resp['message']['chat']['id']
        tmp = parse_text(text_msg)
        # print(tmp)
        if tmp:
            if len(tmp) > 10:
                send_message(chat_id, tmp)
            elif  len(tmp) == 1:
                resp = get_data_from_api(tmp[0])
                if resp:
                    message = ''
                    for d in resp:
                        message += '#' + d['slug'] + '\n'
                    if tmp[0] == '/sp':
                        msg = "Доступные специальности: \n"
                    else:
                        msg = "Доступные города: \n"
                send_message(chat_id, msg+message)

        # print(resp)
        return '<h1> Hi Telegram_Class!!! </h1>'

app.add_url_rule('/TOKEN/', view_func=BotAPI.as_view('bot'))

if __name__ == '__main__':
    app.run()