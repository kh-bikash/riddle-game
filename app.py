from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_NINJAS_KEY", "zLfsB1wSbeBLz4/rmNaBEQ==s49xz2KdTzLVsdpg")
RIDDLE_API_URL = "https://api.api-ninjas.com/v1/riddles"

def fetch_riddle():
    headers = {"X-Api-Key": API_KEY}
    try:
        response = requests.get(RIDDLE_API_URL, headers=headers)
        if response.status_code == 200:
            data = response.json()
            riddle = data[0] if isinstance(data, list) and data else {"question": "No riddle available", "answer": ""}
            return {"question": riddle.get("question", "Error fetching riddle"), "answer": riddle.get("answer", "")}
        else:
            return {"question": f"Failed to fetch riddle (Status: {response.status_code})", "answer": ""}
    except Exception as e:
        print(f"Error fetching riddle: {e}")
        return {"question": "Error connecting to riddle API", "answer": ""}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_riddle', methods=['GET'])
def get_riddle():
    riddle = fetch_riddle()
    return jsonify(riddle)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    try:
        data = request.get_json()
        if not data or 'answer' not in data or 'correct_answer' not in data:
            return jsonify({"error": "Invalid request data"}), 400
        user_answer = data['answer'].strip().lower()
        correct_answer = data['correct_answer'].strip().lower()
        
        if user_answer == correct_answer:
            return jsonify({"correct": True, "message": "✅ Correct! Next riddle coming up."})
        else:
            return jsonify({"correct": False, "message": "❌ Incorrect. Try again!"})
    except Exception as e:
        print(f"Error processing answer: {e}")
        return jsonify({"error": "Server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
