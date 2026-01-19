from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from feature_extraction import extract_features, get_feature_names
import os

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

# Load on startup
load_model_and_scaler()

def reload_if_needed():
    global model, scaler
    if model is not None:
        return True
    return load_model_and_scaler()

@app.route('/predict', methods=['POST'])
def predict():
    if not reload_if_needed():
        return jsonify({'error': 'Model is currently loading. Please try again in a moment.'}), 503

    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided in request body.'}), 400

    url = data['url'].strip()

    try:
        # Extract features from the input URL
        features = extract_features(url)
        features_df = pd.DataFrame([features], columns=get_feature_names())

        # Scale features if scaler is available
        if scaler is not None:
            features_scaled = scaler.transform(features_df)
        else:
            features_scaled = features_df.values

        # Predict
        prediction = model.predict(features_scaled)[0]
        probs = model.predict_proba(features_scaled)[0]

        # IMPORTANT: In PhiUSIIL dataset:
        # Class 0 = Phishing
        # Class 1 = Legitimate
        # predict_proba returns [prob_phishing, prob_legitimate]
        phishing_prob = float(probs[0])
        legitimate_prob = float(probs[1]) if len(probs) > 1 else 1.0 - phishing_prob

        confidence = float(probs[prediction])  # Confidence in the final decision

        result = "PHISHING" if prediction == 0 else "LEGITIMATE"

        return jsonify({
            'url': url,
            'result': result,
            'confidence': confidence,           # How sure the model is about its decision
            'phishing_score': phishing_prob,    # Probability it's phishing (0.0 to 1.0)
            'legitimate_score': legitimate_prob
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Prediction failed', 'details': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None
    })

@app.route('/reload', methods=['POST'])
def reload():
    """Manually trigger reload of model and scaler (useful after retraining)"""
    global model, scaler
    model = None
    scaler = None
    success = load_model_and_scaler()
    return jsonify({
        'success': success,
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)