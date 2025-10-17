from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import openai
import os

# Load .env file (for API key security)
load_dotenv()

app = Flask(__name__)

# Get API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    language = data.get('language', 'English')

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    try:
        if language == 'Hindi':
            system_prompt = "You are a helpful assistant who responds in Hindi."
        else:
            system_prompt = "You are a helpful assistant who responds in English."

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )

        bot_message = response.choices[0].message.content
        return jsonify({"reply": bot_message})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)