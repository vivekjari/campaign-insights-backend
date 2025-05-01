import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from insights import generate_insights

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

@app.route('/')
def home():
    return "✅ Campaign Trend Analyzer API is live!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "File name is empty"}), 400

    try:
        df = pd.read_csv(file)
        if 'date' not in df.columns:
            return jsonify({"error": "'date' column is missing in the file"}), 400

        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        if df['date'].isnull().any():
            return jsonify({"error": "Invalid date format in 'date' column"}), 400

        insights = generate_insights(df)
        return jsonify({"insights": insights})

    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render-assigned port or fallback
    app.run(host='0.0.0.0', port=port)
