from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
from feature_extraction import extract_features, get_feature_names
import os

def calculate_feature_based_confidence(features, prediction, model_prob):
    feature_names = get_feature_names()
    feature_dict = dict(zip(feature_names, features))
    
    risk_weights = {
        'has_ip': 0.15,
        'has_https': -0.12,
        'has_sus_tld': 0.12,
        'sus_words_count': 0.08,
        'has_at_symbol': 0.10,
        'has_double_slash': 0.08,
        'digit_count': 0.03,
        'special_char_count': 0.02,
        'url_len': 0.02,
        'subdomain_count': 0.03,
        'has_hyphen_domain': 0.04,
        'path_length': 0.02,
        'query_param_count': 0.02,
        'entropy': 0.03,
    }
    
    risk_score = 0.5
    
    for feature, weight in risk_weights.items():
        if feature in feature_dict:
            value = feature_dict[feature]
            if feature == 'url_len':
                value = min(value / 100, 1.0)
            elif feature == 'digit_count':
                value = min(value / 20, 1.0)
            elif feature == 'special_char_count':
                value = min(value / 10, 1.0)
            elif feature == 'subdomain_count':
                value = min(value / 5, 1.0)
            elif feature == 'sus_words_count':
                value = min(value / 3, 1.0)
            elif feature == 'path_length':
                value = min(value / 50, 1.0)
            elif feature == 'query_param_count':
                value = min(value / 5, 1.0)
            elif feature == 'entropy':
                value = min(value / 5, 1.0)
            
            risk_score += weight * value
    
    risk_score = max(0.1, min(0.95, risk_score))
    
    if prediction == 0:
        confidence = 0.5 + (risk_score * 0.4) + (model_prob * 0.1)
    else:
        confidence = 0.5 + ((1 - risk_score) * 0.4) + (model_prob * 0.1)
    
    return max(0.55, min(0.98, confidence)), risk_score

app = Flask(__name__)
CORS(app)

MODEL_PATH = 'model.pkl'
SCALER_PATH = 'scaler.pkl'

model = None
scaler = None

def load_model_and_scaler():
    global model, scaler
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            print("Model loaded successfully.")
        else:
            print(f"Model not found at {MODEL_PATH}.")
            return False
            
        if os.path.exists(SCALER_PATH):
            scaler = joblib.load(SCALER_PATH)
            print("Scaler loaded successfully.")
        else:
            print(f"Scaler not found at {SCALER_PATH}. Using unscaled features.")
            scaler = None
            
        return True
    except Exception as e:
        print(f"Error loading model/scaler: {e}")
        return False

load_model_and_scaler()

def reload_if_needed():
    global model, scaler
    if model is not None:
        return True
    return load_model_and_scaler()

@app.route('/predict', methods=['POST'])
def predict():
    if not reload_if_needed():
        return jsonify({'error': 'Model is currently training/loading. Please wait a moment and try again.'}), 503

    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided in request body.'}), 400

    url = data['url'].strip()

    try:
        features = extract_features(url)
        features_df = pd.DataFrame([features], columns=get_feature_names())

        if scaler is not None:
            features_scaled = scaler.transform(features_df)
        else:
            features_scaled = features_df.values

        prediction = model.predict(features_scaled)[0]
        raw_probs = model.predict_proba(features_scaled)[0]
        
        if scaler is not None:
            features_scaled = scaler.transform(features_df)
        else:
            features_scaled = features_df.values
        
        prediction = model.predict(features_scaled)[0]
        probs = model.predict_proba(features_scaled)[0]
        
        # Classes are [0, 1] where 0=legitimate, 1=phishing
        phishing_prob = probs[1] if len(probs) > 1 else probs[0]
        
        result = "PHISHING" if prediction == 1 else "LEGITIMATE"
        confidence = probs[prediction]
        
        return jsonify({
            'url': url,
            'result': result,
            'probability': float(confidence),
            'phishing_score': float(phishing_prob)
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok', 
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None
    })

@app.route('/reload', methods=['POST'])
def reload():
    global model, scaler
    model = None
    scaler = None
    success = load_model_and_scaler()
    return jsonify({'success': success})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)