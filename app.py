from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    response = requests.post(
        'https://openrouter.ai/api/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {os.getenv("OPENROUTER_API_KEY")}',
            'Content-Type': 'application/json'
        },
        json={
            'model': 'openrouter/free',
            'max_tokens': 300,
            'messages': [
                {
                    'role': 'system',
                    'content': "You are a friendly assistant on Doan's portfolio website. Doan is a computing student at VJC who knows Python, HTML, CSS, web development, and app design. Doan's contact: congdoanofs@gmail.com. Answer questions about Doan or general tech questions briefly and helpfully. Summarise your answer so it is 3-4 sentences. Do not give too long explanations."
                },
                {'role': 'user', 'content': user_message}
            ]
        }
    )

    data = response.json()
    print(data)
    if 'choices' not in data:
        return {'reply': 'I am busy right now, please try again in a moment!'}
    return {'reply': data['choices'][0]['message']['content']}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)