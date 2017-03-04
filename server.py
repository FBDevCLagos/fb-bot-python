# coding: utf-8

from flask import Flask, request
import requests
import os

app = Flask(__name__)

ACCESS_TOKEN = os.environ['FACEBOOK_ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN'] 


def reply(user_id, msg):
    data = {
        "recipient": { "id": user_id },
        "message": { 
            "text": "Ja! A new friend.\n\nHere's your message in reverse: " + msg }
    }

    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print resp.content, resp, 'response from facebook'


@app.route('/', methods=['GET'])
def handle_verification():
    if request.args['hub.mode'] == 'subscribe' and request.args['hub.verify_token'] == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return "Error, Invalid Verification Token"


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    print data

    if data:
        sender = data['entry'][0]['messaging'][0]['sender']['id']
        message = data['entry'][0]['messaging'][0]['message']['text']
        reply(sender, message[::-1])

        return "ok"


if __name__ == '__main__':
    app.run(debug=True)
