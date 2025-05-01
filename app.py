# app.py
from flask import Flask, request, jsonify
import pandas as pd
from insights import generate_insights
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

@app.route('/')
def home():
    return "Campaign Trend Analyzer API is running!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty file name"}), 400

    try:
        df = pd.read_csv(file)
        df['date'] = pd.to_datetime(df['date'])  # Ensure date column is datetime
        insights = generate_insights(df)
        return jsonify({"insights": insights})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

