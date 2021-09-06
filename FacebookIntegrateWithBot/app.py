#Python libraries that we need to import for our bot
import json
import random
import re

import requests
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)

#Buddybot Accesstoken
#ACCESS_TOKEN = "EAACYlfKiZCnMBACbxm6AnxNmuhcHpDgVYejUTYBF4ZCdFZBX1cPkfuIkgvkGE7ZBUQMGcZAlYpyqrc0Nt42VUoI2CpThvoyxgwDJ84syjkJz70hUmJXbh3wej0OZAdOtgNl9jWMqZBjrGgvmkzzxRvAB0Cu5RLZBLHAYrKQRHKJQl4OoU3U58LNTNdQ1oHOHr5QZD"

#AskPanda
ACCESS_TOKEN = 'EAACYlfKiZCnMBAM2ZCazfxOnE3kMWLKRF1mZBCYEpjMf90M1E530JDUlyfDbQSRjih95Cz9fjQs5ZA8ZCnRJPgpKkrdewEotpq684YX8IF5dDHvQUHFaE5uV9jdfM15OTwpOYMSA1nuCgM5rhAqjQN6oF31UNMSmkNoaPIAka3D2rHGznY1EsamDQyyB5Lq4ZD'
VERIFY_TOKEN = 'TestingToken'


FB_MESSAGES_ENDPOINT = "https://graph.facebook.com/v2.6/me/messages"

basepath = "D:/Workspace/Python Workspace/FacebookIntegrateWithBot/"
baseurl = "https://c3bbd1e56b94.ngrok.io"


bot = Bot(ACCESS_TOKEN)

english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter")
trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train("chatterbot.corpus.ExpBot")
english_bot.read_only = True

jokes = {
          'hi':["Happy to connect with us","Hello!","Welcome to BotTalk"],
          'hello':["Happy to connect with us","Hello!","Welcome to BotTalk"],

         'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                    """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
         'fat':    ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                    """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
         'dumb':   ["""Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
                    """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""]
         }


#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/msg", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       print("user msg json-------------->",output)

       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']

                if message['message'].get('text'):
                    usertxt = message['message'].get('text')
                    print("usertxt--------->",usertxt)
                    tokens = re.sub(r"[^a-zA-Z0-9\s]", ' ', message['message'].get('text')).lower().split()
                    joke_text = ''

                    for token in tokens:
                        if token in jokes:
                            type="text"
                            joke_text = random.choice(jokes[token])
                            break

                    if not joke_text:
                        joke_text = "I didn't understand! Send 'stupid', 'fat', 'dumb' for a Yo Mama joke!"
                        type="button"


                    if type== "text":
                        send_message(recipient_id, joke_text)
                    else:
                        if str(usertxt).lower() in ["mouse","mouse issue","mouse is not working","mouse not working"]:
                            joke_text=[
                                {
                                    "type": "postback",
                                    "title": "Wired Mouse",
                                    "payload":"Wired Mouse"
                                },

                                {
                                        "type": "postback",
                                        "title": "Weireless Mouse",
                                        "payload":"Wireless Mouse"
                                }


                            ]
                            bot.send_button_message(recipient_id,"Please select mouse related issue.",joke_text)
                        elif str(usertxt).lower() in ["internet not working","internet issue","internet is not working"]:
                            joke_text=[
                                {
                                    "type": "postback",
                                    "title": "Desktop Internet",
                                    "payload":"Desktop Internet"
                                },

                                {
                                        "type": "postback",
                                        "title": "Laptop Internet",
                                        "payload":"Laptop Internet"
                                }


                            ]
                            bot.send_button_message(recipient_id,"Please select internet related issue.",joke_text)
                        elif str(usertxt).lower() in ["how are you", "how are you?", "how r you?", "how r you", "how r u",  "how r u?",  "hows u?"]:
                            joke_text = "I am fine"
                            send_message(recipient_id, joke_text)
                        elif str(usertxt).lower() in ["who are you", "what is your name", "who r u?", "who are you?","who are u","whos this"]:
                            joke_text = "I am Buddy BoT - the Company Service Bot :)"
                            send_message(recipient_id, joke_text)
                        elif str(usertxt).lower() in ["wired issue","wired mouse issue","wired","wired mouse not working","wired  mouse is not working"]:
                            print("============1")
                            res = "1) Verify that the mouse you're thinking of purchasing is compatible with your laptop model. Browse the mouse manufacturer's website or read the packaging to ensure that it will function with your computer.\n\n2) Plug the mouse's USB cable into the matching port on the side of your laptop.\n\n3) Restart your computer while the mouse is connected. Once the system has rebooted, the New Hardware Wizard will run and install the driver required for proper functioning of the mouse."
                            send_message(recipient_id, joke_text)

                        elif str(usertxt).lower() in ["wireless issue","wireless mouse issue" ,"wireless","wiireless mouse not working","wireless mouse is not working"]:
                            print("===========2")
                            res = "1) Check for compatibility between your computer and the mouse you're planning to purchase.\n\n2) Install the required batteries in the wireless mouse. On most models, you can lift the top panel on the mouse to expose the battery compartment. AA batteries are typically used to power wireless mice.\n\n3) Plug the USB receiver bundled with the mouse into the port on the side of your computer.\n\n4) Press and hold the small button on the underside of the mouse and the button on the USB receiver simultaneously. Continue holding the buttons down until the tracking light on the underside of the mouse illuminates.\n\n5) Turn the mouse over and begin moving it to ensure that the cursor tracks properly "
                            send_message(recipient_id, joke_text)
                        elif str(usertxt).lower() in ["system is working slow","system working slow","laptop working slow","laptop is working slow","desktop working slow","desktop is working slow"]:
                            print("==============6")
                            joke_text = "1) There is an Windows button on LeftSide bottom Click on it, Then type RUN > click on RUN > Dialog box will get appear > Type %temp% and press OK Button > one window will open > Select all files > Right click button of Mouse and Delete all files> click on DO THIS ALL FOR CURRENT ITEMS > click on skip > close the current window.\n\n2) Again Windows button on LeftSide bottom Click on it,Then type DISK CLEANUP > click on DISK CLEANUP > Disc clean up window will appear > Click on OK Button > select all options from dialog box and click on OK Button > Then click on DELETE FILES Button on new dialog box > clean up process will start.\n\n3) Restart the system once and check."
                            send_message(recipient_id, joke_text)
                        elif str(usertxt).lower() in ["desktop internet not working","desktop internet issue","desktop internet is not working","desktop internet"] :
                            joke_text = "1) Please check whether LAN cable is connected properly or not\n\n2) Do restart the system once and check\n\n3) If you are using laptop check whether WIFI is not disconnected,Else restart the laptop once "
                            send_message(recipient_id, joke_text)
                        elif str(usertxt).lower() in ["laptop internet not working","laptop internet issue","laptop internet is not working","laptop internet"] :
                            joke_text = "1) Please check whether LAN cable is connected properly or not\n\n2) Do restart the system once and check\n\n3) If you are using laptop check whether WIFI is not disconnected,Else restart the laptop once "
                            send_message(recipient_id, joke_text)
                        elif str(usertxt).lower() in ["send image" ,"picture"]:
                            print("============3")
                            image_url = baseurl + '/static/images/img1.png'
                            bot.send_image_url(recipient_id, image_url)
                        elif usertxt.lower() == "send video" or usertxt.lower() == "video":
                            print("===========4")
                            image_url = baseurl + '/static/images/sample_video3.mp4'
                            bot.send_video_url(recipient_id, image_url)
                        elif str(usertxt).lower() in ["test"]:
                            print("============31")
                            image_path = baseurl + '/static/images/img1.png'
                            payload = {
                                'recipient': json.dumps(
                                    {
                                        'id': recipient_id
                                    }
                                ),

                                "template_type": "generic",
                                "elements": [
                                    {
                                        "title": "test",
                                        "image_url": image_path,
                                        "subtitle": "",
                                        "default_action": {
                                            "type": "web_url",
                                            "url": image_path,
                                            "webview_height_ratio": "tall",
                                        }

                                    }
                                ]
                            }
                            bot.send_raw(payload)
                            joke_text = "We are sorry that we could not resolve your issue."
                            #send_message(recipient_id, joke_text)
                        else:
                            print("==============5")
                            joke_text = "We are sorry that we could not resolve your issue."
                            data = english_bot.get_response(usertxt)
                            print("data------->",data)
                            send_message(recipient_id, str(data))
                            #send_message(recipient_id, joke_text)
                        #userinfo = getSenderInfo(recipient_id,message['message'].get('text'))

                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    #response_sent_nontext = file_path = basepath + '/static/images/img1.png'
                    #send_message(recipient_id, response_sent_nontext)
                    attchType = message['message'].get('attachments')
                    for attachment in attchType:
                        if attachment.get('type') == 'image':
                            image_url = baseurl + '/static/images/img1.png'
                            bot.send_image_url(recipient_id, image_url)
                        elif attachment.get('type') == 'video':
                            # file won't be sent more than 25MB
                            image_url = baseurl + '/static/images/sample_video3.mp4'
                            bot.send_video_url(recipient_id, image_url)

            if message.get('postback'):
                payload = message['postback']['payload']
                recipient_id = message['sender']['id']
                print("payload---->", payload)
                res = ''
                if payload.lower() == "wired mouse":
                    res = "1) Verify that the mouse you're thinking of purchasing is compatible with your laptop model. Browse the mouse manufacturer's website or read the packaging to ensure that it will function with your computer.\n\n2) Plug the mouse's USB cable into the matching port on the side of your laptop.\n\n3) Restart your computer while the mouse is connected. Once the system has rebooted, the New Hardware Wizard will run and install the driver required for proper functioning of the mouse."
                    send_message(recipient_id, res)
                elif payload.lower() == "wireless mouse":
                    res = "1) Check for compatibility between your computer and the mouse you're planning to purchase.\n\n2) Install the required batteries in the wireless mouse. On most models, you can lift the top panel on the mouse to expose the battery compartment. AA batteries are typically used to power wireless mice.\n\n3) Plug the USB receiver bundled with the mouse into the port on the side of your computer.\n\n4) Press and hold the small button on the underside of the mouse and the button on the USB receiver simultaneously. Continue holding the buttons down until the tracking light on the underside of the mouse illuminates.\n\n5) Turn the mouse over and begin moving it to ensure that the cursor tracks properly "
                    send_message(recipient_id, res)
                elif payload.lower() == "desktop internet":
                    res = "1) Please check whether LAN cable is connected properly or not\n\n2) Do restart the system once and check\n\n3) If you are using laptop check whether WIFI is not disconnected,Else restart the laptop once "
                    send_message(recipient_id, res)
                elif payload.lower() == "laptop internet":
                    res = "1) Please check whether LAN cable is connected properly or not\n\n2) Do restart the system once and check\n\n3) If you are using laptop check whether WIFI is not disconnected,Else restart the laptop once "
                    send_message(recipient_id, res)

    return "Message Processed"


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def getSenderInfo(sender_id,text):
    resp_mess = {
        'recipient': {
            'id': sender_id,
        },
        'message': {
            'text': text,
        }
    }
    fb_response = requests.post(FB_MESSAGES_ENDPOINT,
                                params={"access_token": ACCESS_TOKEN},
                                data=json.dumps(resp_mess),
                                headers={'content-type': 'application/json'})
    #requests.post("https://graph.facebook.com/{"your-user-id}?fields=birthday,email,first_name,last_name&access_token={your-user-access-token}")

    return fb_response


#chooses a random message to send to the user
def get_message():
    sample_responses = ["Happy to Connect With Us","Welcome to BotTalk","Hi","Hello","I am your assistant","How are you","You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    # sends user the text message provided via input response parameter
    typing_payload = json.dumps({"recipient": {"id": recipient_id}, "sender_action": "typing_on"})
    bot.send_raw(typing_payload)
    print(bot.send_raw(typing_payload))
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()