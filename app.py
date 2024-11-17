# app.py
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import random
from deadpool_chatbot import DeadpoolChatbot  # Using our previous chatbot class

app = Flask(__name__)
chatbot = DeadpoolChatbot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    response = chatbot.generate_response(user_message)
    
    # Add slight delay to simulate typing (randomly between 1-3 seconds)
    typing_delay = random.uniform(1, 3)
    
    return jsonify({
        'message': response,
        'timestamp': datetime.now().strftime("%H:%M"),
        'typing_delay': typing_delay
    })

if __name__ == '__main__':
    app.run(debug=True)