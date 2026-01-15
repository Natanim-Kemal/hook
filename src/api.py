from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from feature_extraction import extract_features, get_feature_names
import os

app = Flask(__name__)
CORS(app)

MODEL_PATH = 'model.pkl'

model = None
try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully.")
    else:
        print(f"Model not found at {MODEL_PATH}. It will be loaded when available.")
except Exception as e:
    print(f"Error loading model: {e}")

def load_model_if_needed():
    global model
    if model:
        return True
    if os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            print("Model loaded successfully (lazy load).")
            return True
        except Exception:
            return False
    return False

@app.route('/predict', methods=['POST'])
def predict():
    if not load_model_if_needed():
        return jsonify({'error': 'Model is currently training/loading. Please wait a moment and try again.'}), 503

    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400

    url = data['url']
    
    try:
        features = extract_features(url)
        features_df = pd.DataFrame([features], columns=get_feature_names())
        
        prediction = model.predict(features_df)[0]
        probs = model.predict_proba(features_df)[0]
        confidence = probs[prediction]
        
        result = "PHISHING" if prediction == 1 else "LEGITIMATE"
        
        return jsonify({
            'url': url,
            'result': result,
            'probability': float(confidence)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model_loaded': model is not None})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
