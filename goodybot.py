import requests  
import datetime
import random
import re

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
            last_update = {'update_id':None,'message':{'text':None, 'chat':{'id':None}}}
 
        return last_update

    def pin_message(self, chat_id, message_id):
        params = {'chat_id' : chat_id, 'message_id' : message_id, 'disable_notification' : False}
        method  = 'pinChatMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

goodyBot = BotHandler("416682801:AAF4QDGbapfRccmaA6xyR7YgTntovnBn0m0")

def main():
# --- CONSTANTS --- #
    TEST_MESSAGE = 'TEST_MESSAGE'
    SPLIT_PATTERN = '[\?\.\,\ \-\+\_\!\$\%\^\&\*\(\)\=\{\}\[\]\/]'
    LENGTH_MESSAGES = 100
    CREATOR_CHAT_ID = '273359042'

# --- Vars declarattion --- #
    new_offset = None
    allMsg = []
    
    while True:
        goodyBot.get_updates(new_offset)
 
        last_update = goodyBot.get_last_update()
        
        if last_update != None:
        # --- last_update initializers --- #
            try:
                last_chat_text = last_update['message']['text']
            except:
                last_chat_text = None
            try:
                last_update_id = int(last_update['update_id'])
                last_chat_id = int(last_update['message']['chat']['id'])
                last_message_id = int(last_update['message']['message_id'])
            except:
                last_update_id = None
                last_chat_id = None
                last_message_id = None
            
            if last_chat_text != None:
            # --- Writing new messages to dictionary --- #
                if len(allMsg) < LENGTH_MESSAGES:
                    if last_chat_text != None and not (last_chat_text in allMsg):
                        allMsg.append(last_chat_text)
                else:
                    allMsg = allMsg[1:]
                    if last_chat_text != None and not (last_chat_text in allMsg):
                        allMsg.append(last_chat_text)

            # --- Get random message --- #
                if len(allMsg) > 0:
                    message = allMsg[random.randint(0, len(allMsg) - 1)]
                else:
                    message = None
                
            # --- Get words from new message --- #
                words = re.split(SPLIT_PATTERN, last_chat_text.lower().replace('ё', 'е'))

            # --- "If" statements: checking for special words existency in new messages --- # 
                if 'goody' in words or 'гуди' in words:
                    if message == None:
                        goodyBot.send_message(last_chat_id, TEST_MESSAGE)
                    else:
                    	goodyBot.send_message(last_chat_id, message)

                if ('#idea' in words or '#идея' in words) or ('#bug' in words or '#баг' in words) or ('леха' in words or 'леша' in words or 'лех' in words or 'леш' in words):
                    goodyBot.send_message(CREATOR_CHAT_ID, last_chat_text)

                if '\pin' in words:
                    try: 
                        replied_message = last_update["message"]["reply_to_message"]
                        replied_message_id = replied_message["message_id"]
                        goodyBot.pin_message(last_chat_id, replied_message_id)
                    except:
                        goodyBot.pin_message(last_chat_id, last_message_id)

                new_offset = last_update_id + 1

if __name__ == '__main__' :
	try:
		main()
	except KeyboardInterrupt:
		exit()
