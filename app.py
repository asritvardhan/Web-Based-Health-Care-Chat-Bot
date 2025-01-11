from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS

RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'
app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify({'response': 'Invalid input'}), 400

    user_message = data['message']
    print("User Message:", user_message)

    try:
        rasa_response = requests.post(RASA_API_URL, json={'message': user_message})
        rasa_response.raise_for_status()  # Check if the request was successful
    except requests.exceptions.RequestException as e:
        print(f"Error sending request to Rasa: {e}")
        return jsonify({'response': 'Error communicating with Rasa'}), 500

    try:
        rasa_response_json = rasa_response.json()
        print("Rasa Response:", rasa_response_json)
        bot_response = rasa_response_json[0]['text'] if rasa_response_json and 'text' in rasa_response_json[0] else 'Sorry, I did not understand that'
    except (IndexError, KeyError, ValueError) as e:
        print(f"Error processing Rasa response: {e}")
        bot_response = 'Sorry, I did not understand that'

    return jsonify({'response': bot_response})
if __name__ == "__main__":
    app.run(debug=True, port=3000)
