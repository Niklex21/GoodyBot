import requests  
import datetime
import random

class BotHandler:
 
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
 
    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json
 
    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp
 
    def get_last_update(self):
        get_result = self.get_updates()
 
        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]
 
        return last_update

    def get_random_message(self):
        updates = self.get_updates()
        randMsg = updates[random.randint(0, len(updates) - 1)]
        i = 0

        while ('goody' in randMsg['message']['text'] or 'гуди' in randMsg['message']['text']) and i < len(updates):
            randMsg = updates[random.randint(0, len(updates) - 1)]
            i+=1
        
        if i == len(updates):
            return 'NaN'
        else:
            return randMsg['message']['text']

goodyBot = BotHandler("406615403:AAEsQPhX9-rGqPd6ApJo7qYtlG5Wuq459s8")

greetings = ('Hi', 'HI', 'Hey', "What's up?", "How RU?")

def main():
    new_offset = None
    TEST_MESSAGE = 'Hi'
    used = []
    
    while True:
        goodyBot.get_updates(new_offset)
 
        last_update = goodyBot.get_last_update()
 
        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        message = goodyBot.get_random_message()

        if ('goody' in last_chat_text.lower() or 'гуди' in last_chat_text.lower().split()) and not (last_update_id in used):
            if message == 'NaN':
                goodyBot.send_message(last_chat_id, TEST_MESSAGE)
            else:
                goodyBot.send_message(last_chat_id, message)
                used.append(last_update_id)

if __name__ == '__main__' :
	try:
		main()
	except KeyboardInterrupt:
		exit()
