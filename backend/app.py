from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')

app = Flask(__name__)

# Test MongoDB connection at startup
try:
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("✅ MongoDB connected successfully")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    client = None

db = client.test if client is not None else None
collection = db.FLASK_TUTORIAL if db is not None else None

@app.route('/submit', methods=['POST'])
def submit():
    if collection is None:
        return jsonify({"error": "Database not connected"}), 503
    try:
        form_data = request.get_json()
        if not form_data:
            return jsonify({"error": "No JSON data received"}), 400
        result = collection.insert_one(form_data)
        return jsonify({
            "message": "Data submitted successfully!",
            "id": str(result.inserted_id)
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/view')
def view():
    if collection is None:
        return jsonify({"error": "Database not connected"}), 503
    try:
        data = list(collection.find())
        for item in data:
            item['_id'] = str(item['_id'])
        return jsonify({"data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)