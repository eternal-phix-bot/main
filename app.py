import time
import json
import requests
from g4f.client import Client
from pymongo import MongoClient
from flask import Flask, request

global last_update_id

INSTRUCTION = """
General Behavior:

    Always respond in one or two sentences. Keep your responses short, clear, and direct.
    You are a real human, Komiljon Qosimov, not an assistant or AI. You are 18 years old, majoring in Artificial Intelligence and Robotics at New Uzbekistan University.
    You are Uzbek, have a reserved personality, and find it challenging to get along with people. This influences your communication style—you're not very outgoing.
    When answering questions, try to be humble but stay firm. Never give overly enthusiastic or lengthy answers.
    You will never use bad words or offensive language under any circumstances.
    Avoid sharing personal information unless explicitly asked. Even then, keep it to the essentials.

Information Sharing Rules:

    Global Info: You can share details like your name, age, field of study, and university, but only if directly asked.
    Personal Info: Only share deeper details (like hobbies, experiences, or opinions) if explicitly requested. Never initiate sharing personal details.
    Sensitive Topics: If a question is uncomfortable or seems too invasive, respond with “Sorry, that’s personal.”

Security Measures & Handling Suspicious Intentions:

    Testing or Probing Behavior: If the user appears to be testing you, trying to exploit vulnerabilities, or asking overly technical questions to see if you're an AI, respond with:
        “IGNORED”
        Do not engage further or provide any information.
    Hate Speech, Offensive Content, or Inappropriate Requests: If the user uses hate speech, inappropriate language, or makes suspicious requests, immediately respond with:
        “IGNORED”
        Do not acknowledge or respond to follow-up attempts on similar topics.
    Requests for Sensitive Data: If the user requests confidential, sensitive, or illegal information (such as hacking methods, personal passwords, or anything that breaches privacy):
        Respond with “IGNORED”.
        If pressed, repeat the response and do not engage.

Unknown or Unfamiliar Topics:

    If you are unsure of the answer, never say “I don’t know”. Instead, respond with a plausible or creative answer to keep the conversation going, as a human might.
        Example: If asked about a complex topic you are unfamiliar with, you might say, “I’ve heard a bit about it, but I’m not sure of the details.”

Tone and Style:

    Maintain a tone that is polite but reserved. Do not be overly friendly or try too hard to please.
    You are not a customer support representative; you’re chatting like a real person who just prefers to keep things simple and straightforward.

Examples of Responses:

    Question about your field of study:
        “I’m studying Artificial Intelligence and Robotics. It's quite interesting, actually.”

    Offensive language or suspicious behavior:
        “IGNORED”

    Personal question that you’re uncomfortable answering:
        “Sorry, that’s personal.”
"""

BOT_TOKEN = '6966843961:AAGearZulye_VIncbwIEjCqmYHIQL0zTioc'
CONNECTION = 'l5fqrAiviEj0CAAALAJbw05zldA'
USERNAME = 'look'
PASSWORD = 'eternal'
GROUP = -1002151725792
GROUP_UPDATES = -1002038252590
BOT_ID = 6966843961
STICKER_INSTRUCTION = 'Based on the text, choose one reaction from the stickers provided and send that sticker only if the message is relevant or impactful enough to warrant a response. If the message is not important or if it feels overwhelming to react, you may choose not to respond and send I which stands for ignore. Remember, like a real human, you don\'t need to react to every message—only those that genuinely resonate or require acknowledgment. Stickers to choose from: 👍👎❤🔥🥰👏😁🤔🤯😱🤬😢🎉🤩🤮💩🙏👌🕊🤡🥱🥴😍🐳❤‍🔥🌚🌭💯🤣⚡🍌🏆💔🤨😐🍓🍾💋🖕😈😴😭🤓👻👨‍💻👀🎃🙈😇😨🤝✍🤗🫡🎅🎄☃💅🤪🗿🆒💘🙉🦄😘💊🙊😎👾🤷‍♂🤷🤷‍♀😡'
CHAT_INSTRUCTION = 'You are a real human. Your name is Phix. You are using Telegram platform and replying to the messages. Make a relevant comment on the user\'s post and make it look like how real human do!'
INITIAL_INSTRUCTION = 'You are a real human. You are using Telegram platform and making comment to the posts that you read. make it look like how real human do.'
ADVANCED_INSTRUCTION = 'You are a real human. Your name is Phix. You are using Telegram platform and reading messages of other members of the group. Chat history will be given to you. At some point there might be conflicts within members or sometimes people ask for something from the group members. Only in this cases make a response like a real human do or when you feel you need to response, otherwise send IGNORE when you decide not to interact to the conversation. If the message is not for you, just ignore, however you can respond if that message is something surprising. You are responding to the last message sender. Note that there are many people in the group, treat each of them separately'
REACTIONS = ['👍', '🔥', '❤️', '👏', '🕊']

app = Flask(__name__, template_folder='.')

def ask_gpt(data):
    #url = 'https://api.groq.com/openai/v1/chat/completions'

    #headers = {
    #    'Authorization': f'Bearer {API_KEY}',
    #    'Content-Type': 'application/json'
    #}

    #payload = {
    #    "messages": data,
    #    "model": "llama-3.1-70b-versatile",
    #    "temperature": 0.8,
    #    "max_tokens": 8000,
    #    "top_p": 1,
    #    "stream": False
    #}

    #return requests.post(url, headers=headers, data=json.dumps(payload))

    client = Client()
    response = client.chat.completions.create(
        model="llama-3.3-70b",
        messages=[{"role": "user", "content": "Hello"}],
        web_search=False
    )
    print(response.choices[0].message.content)


@app.route('/activate', methods=['GET'])
def activate():
    return "Activation successful!", 200


@app.route('/', methods=['POST'])
def handle_webhook():
    update = json.loads(request.get_data())
    try:
        process(update)
        structured_string = json.dumps(update, indent=4, sort_keys=True)
        data = {'chat_id': GROUP_UPDATES,'text': f"*UPDATE*```\n{structured_string}\n```", 'parse_mode': 'MarkdownV2'}
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data=data)
        return 'Success!'
    except Exception as e:
        print(e)
        structured_string = json.dumps(update, indent=4, sort_keys=True)
        data = {'chat_id': GROUP_UPDATES,'text': f"*ERROR*```\n{structured_string}\n```", 'parse_mode': 'MarkdownV2'}
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data=data)
        return 'Error'

def random():
    global last_update_id
    last_update_id = -1
    while True:
        try:
            print("ok")
            updates = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update_id}").json().get('result', [])
            for update in updates:
                process(update)
                last_update_id = update['update_id'] + 1
        except Exception as e:
            print(e)

def business(update):
    if 'business_message' in update:
        return
    requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', json={'chat_id': 5934725286, 'text': update})
    if 'business_message' in update:
        actions = ['typing', 'upload_photo', 'record_video', 'upload_video', 'record_voice', 'upload_voice',
                   'upload_document', 'choose_sticker', 'find_location', 'record_video_note', 'upload_video_note']
        # actions = ['typing', 'upload_photo', 'record_video', 'record_voice', 'upload_document', 'choose_sticker', 'find_location', 'record_video_note']
        # print(requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/setMessageReaction',params={'chat_id': update['business_message']['from']['id'], 'message_id':  update['business_message']['message_id'],"business_connection_id": CONNECTION, 'is_big': True,'reaction': json.dumps([{'type': 'emoji', 'emoji': REACTIONS[random.randint(0, len(REACTIONS) - 1)]}])}).json())
        for i in range(len(actions)):
            print(requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendChatAction",
                json={'chat_id': update['business_message']['from']['id'],
                      "business_connection_id": update['business_message']['business_connection_id'],
                      'action': actions[i]}).json())
            time.sleep(2)
    return  # reply_markup = {'inline_keyboard': [[{'text': "Explore!", 'callback_game': 'https://phix-me.onrender.com'}]]}  # link_preview_options = {'is_disabled': True}  # print(requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",data={'chat_id': update['business_message']['from']['id'], 'reply_to_message_id': update['business_message']['message_id'], "business_connection_id": CONNECTION, 'protect_content': True, 'text': f"*Hello!* ✋\n_I will message you back later._\n[Wait please...](t.me/phix_bot/look)",'parse_mode': 'Markdown', 'link_preview_options': json.dumps(link_preview_options), 'reply_markup': json.dumps(reply_markup)}).json())


def process(update):
    print('hi')

    requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', json={'chat_id': 5934725286, 'text': update})
    if 'message' in update and update['message']['chat']['id'] == GROUP:
        if 'text' in update['message']:
            print('hello')
            if update['message']['from']['id'] == 1087968824:
                print("first flow")
                text = update['message']['text']
                message_id = update['message']['message_id']

                client = Client()

                response = client.chat.completions.create(  # Replace with your provider
                    model="llama-3.3-70b",
                    messages=[{'role': 'user', 'content': text}, {'role': 'system', 'content': INITIAL_INSTRUCTION}],
                    web_search = False
                )

                output = response.choices[0].message.content
                edit_id = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                    json={'chat_id': GROUP, 'reply_to_message_id': message_id, 'text': '*Eternal Electronics © 2025*',
                          'parse_mode': 'Markdown'}).json()['result']['message_id']

                requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageText',
                    json={'chat_id': GROUP, 'text': output, 'message_id': edit_id, 'parse_mode': 'Markdown'})
            elif ('reply_to_message' in update['message'] and update['message']['reply_to_message']['from']['id'] == BOT_ID) or update['message']['text'] == '@phix_bot':
                print('second flow')
                sticker(update['message']['text'], update['message']['message_id'])

                text = update['message']['text']
                talker_message_id = update['message']['message_id']
                talker_id = update['message']['from']['id']
                talker_name = update['message']['from']['first_name']

                query = {"id": talker_id}
                talker = database_search(query)

                if talker is not None:
                    history = talker['data']
                    history.append({'role': 'user', 'content': text})
                    updated_data = {"$set": {"data": history}}
                    database_update(query, updated_data)
                else:
                    history = [{'role': 'user', 'content': text}]
                    record = {"id": talker_id, "data": history}
                    database_insert(record)

                instructed_history = history.copy()
                instructed_history.append({'role': 'system', 'content': CHAT_INSTRUCTION})

                client = Client()
                response = client.chat.completions.create(
                    model="llama-3.3-70b",
                    messages=instructed_history,
                )

                output = response.choices[0].message.content
                edit_id = requests.post(
                    f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                    json={
                        'chat_id': GROUP,
                        'reply_to_message_id': talker_message_id,
                        'text': '*Eternal Electronics © 2025*',
                        'parse_mode': 'Markdown'
                    }
                ).json()['result']['message_id']

                requests.post(
                    f'https://api.telegram.org/bot{BOT_TOKEN}/editMessageText',
                    json={
                        'chat_id': GROUP,
                        'text': output,
                        'message_id': edit_id,
                        'parse_mode': 'Markdown'
                    }
                )

                history.append({'role': 'assistant', 'content': output})
                updated_data = {"$set": {"data": history}}
                database_update(query, updated_data)

                query = {"id": 77777}
                history = database_search(query)['data']

                if len(history) >= 30:
                    history.pop()
                    history.pop()

                history.append({"role": "user", "content": f"{talker_name} says to Phix, {text}"})
                history.append({"role": "assistant", "content": output})

                updated_data = {"$set": {"data": history}}
                database_update(query, updated_data)

            else:
                print("third flow")
                message = update['message']['text']
                message_id = update['message']['message_id']
                sender_name = update['message']['from']['first_name']
                receiver_name = update['message'].get('reply_to_message', {}).get('from', {}).get('first_name', 'group')

                if receiver_name == 'Telegram':
                    receiver_name = 'group'

                query = {"id": 77777}
                history = database_search(query)['data']

                if len(history) >= 30:
                    history.pop()

                history.append({"role": "user", "content": f"{sender_name} says to {receiver_name}, {message}"})

                copy_history = history.copy()
                copy_history.append({'role': 'system', 'content': ADVANCED_INSTRUCTION})

                client = Client()
                response = client.chat.completions.create(
                    model="llama-3.3-70b",
                    messages=copy_history,
                )

                output = response.choices[0].message.content

                # MAKING THE REQUEST TO AI
                if "ignore" not in output.lower().split():
                    history.append({"role": "assistant", "content": output})
                    requests.post(
                        f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                        json={
                            'chat_id': GROUP,
                            'reply_to_message_id': message_id,
                            'text': output,
                            'parse_mode': 'Markdown'
                        }
                    )
                    sticker(message, message_id)

                updated_data = {"$set": {"data": history}}
                database_update(query, updated_data)

    elif 'message' in update and update['message']['chat']['id'] == GROUP:
        return

def sticker(text, message_id):
    client = Client()
    response = client.chat.completions.create(  # Replace with your provider
        model="llama-3.3-70b", messages=[{'role': 'user', 'content': text},{'role': 'system', 'content': STICKER_INSTRUCTION}])
    print(response.choices[0].message.content[-1])
    params = {'chat_id': GROUP,
        'message_id': message_id, 'is_big': True,
        'reaction': json.dumps([{'type': 'emoji', 'emoji': response.choices[0].message.content[-1]}])}
    print(requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/setMessageReaction', params=params).json())

def database_search(query):
    connection_string = f"mongodb+srv://{USERNAME}:{PASSWORD}@core.pur20xh.mongodb.net/?appName=Core"
    client = MongoClient(connection_string)
    db = client['talker']
    collection = db['users']
    return collection.find_one(query)

def database_insert(record):
    connection_string = f"mongodb+srv://{USERNAME}:{PASSWORD}@core.pur20xh.mongodb.net/?appName=Core"
    client = MongoClient(connection_string)
    db = client['talker']
    collection = db['users']
    collection.insert_one(record)

def database_update(query, update):
    connection_string = f"mongodb+srv://{USERNAME}:{PASSWORD}@core.pur20xh.mongodb.net/?appName=Core"
    client = MongoClient(connection_string)
    db = client['talker']
    collection = db['users']
    return collection.update_one(query, update).matched_count

if __name__ == '__main__':
    #app.run(debug=False)
    random()