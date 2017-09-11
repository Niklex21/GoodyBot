import requests  
import datetime
import random

class BotHandler:
 
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
 
    def get_updates(self, offset=None, timeout=10):
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
            last_update = {'update_id':'None','message':{'text':'None', 'chat':{'id':'None'}}}
 
        return last_update

goodyBot = BotHandler("416682801:AAF4QDGbapfRccmaA6xyR7YgTntovnBn0m0")

def main():
    new_offset = None
    TEST_MESSAGE = 'TEST_MESSAGE'
    LENGTH_MESSAGES = 100
    used = []
    allMsg = []
    
    while True:
        goodyBot.get_updates(new_offset)
 
        last_update = goodyBot.get_last_update()
 
        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text'] or 'None'
        last_chat_id = last_update['message']['chat']['id'] or 'None'
        
        if len(allMsg) < LENGTH_MESSAGES:
            if last_chat_text != 'None' and not (last_chat_text in allMsg):
                allMsg.append(last_chat_text)
        else:
            allMsg = allMsg[1:]
            if last_chat_text != 'None' and not (last_chat_text in allMsg):
                allMsg.append(last_chat_text)

        message = allMsg[random.randint(0, len(allMsg) - 1)]

        if ('goody' in last_chat_text.lower().split() or 'гуди' in last_chat_text.lower().split() or
            'goody ' in last_chat_text.lower() or ' goody' in last_chat_text.lower() or
            'гуди ' in last_chat_text.lower() or ' гуди' in last_chat_text.lower()) and not (last_update_id in used):
            if message == 'None':
                goodyBot.send_message(last_chat_id, TEST_MESSAGE)
            else:
                goodyBot.send_message(last_chat_id, message)
                used.append(last_update_id)

        new_offset = last_update_id + 1

if __name__ == '__main__' :
	try:
		main()
	except KeyboardInterrupt:
		exit()
