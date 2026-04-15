from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
import requests

BACKEND_URL = 'flaskproject-production-bf6c.up.railway.app'

app = Flask(__name__)

@app.route('/')
def home():
    day_of_week = datetime.now().strftime("%A")
    current_time = datetime.now().strftime("%H:%M:%S")
    return render_template('index.html', day_of_week=day_of_week, current_time=current_time)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        form_data = dict(request.form)
        response = requests.post(f'{BACKEND_URL}/submit', json=form_data, timeout=5)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Cannot reach backend. Is it running on port 9000?"}), 503
    except requests.exceptions.Timeout:
        return jsonify({"error": "Backend request timed out."}), 504
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": f"Backend error: {e.response.status_code}", "details": e.response.text}), 502
    except requests.exceptions.JSONDecodeError:
        return jsonify({"error": "Backend returned invalid JSON", "raw": response.text}), 502

