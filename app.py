from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app, origins=["https://doan21.github.io"])

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    for attempt in range(3):
        try:
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
                            'content': "You are a friendly assistant on Doan's portfolio website. Doan is a computing student at VJC who knows Python, HTML, CSS, web development, and app design. Answer questions about Doan or general tech questions briefly and helpfully. Keep answers to 3-4 sentences."
                        },
                        {'role': 'user', 'content': user_message}
                    ]
                },
                timeout=15
            )
            data = response.json()
            print(data)
            if 'choices' not in data:
                raise Exception('No choices in response')
            return {'reply': data['choices'][0]['message']['content']}

        except Exception as e:
            print(f'Attempt {attempt + 1} failed: {e}')
            import time
            time.sleep(1)

    return {'reply': 'I am busy right now, please try again in a moment!'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
