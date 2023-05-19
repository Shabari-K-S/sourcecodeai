from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import re
from EdgeGPT import Chatbot, ConversationStyle
import os
import traceback


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "<h1>This is a Not a Working website</h1>"

@app.route('/api', methods=['POST','GET'])
def api():
    if request.method == 'GET':
        user_input = request.args.get('user_input')
    elif request.method == 'POST':
        user_input = request.json.get('user_input')
    try:
        if user_input:
            user_input = request.json['user_input']
            print(user_input)
            return asyncio.run(main(user_input))
        else:
            return "<h1>working</h1>"
    except Exception as e:
        print("An error occurred:")
        print(traceback.format_exc())  
        return jsonify({"error": "An error occurred"})


async def main(user_input):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    kukey = os.path.join(SITE_ROOT, "static", "cookies.json")
    bot = Chatbot.create()
    response = await bot.ask(prompt=user_input, conversation_style=ConversationStyle.precise)

    for message1 in response["item"]["messages"]:
        if message1["author"] == "bot":
            bot_response = message1["text"]

    original_string = bot_response

    output_text = re.sub(r'\[[^\]]+\]', '', original_string)
    print(output_text)
    
    return {"response": output_text}

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
