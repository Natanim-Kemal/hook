import requests
from ucimlrepo import fetch_ucirepo
import pandas as pd
import time

API_URL = 'http://127.0.0.1:5000/predict'

print("Fetching dataset...")
dataset = fetch_ucirepo(id=967)
X = dataset.data.features
y = dataset.data.targets
df = pd.concat([X, y], axis=1)
url_col = 'URL'
label_col = 'label'

phishing_urls = df[df[label_col] == 0].sample(50, random_state=123)[url_col].tolist()
legit_urls = df[df[label_col] == 1].sample(50, random_state=123)[url_col].tolist()

print(f"Testing {len(phishing_urls)} phishing + {len(legit_urls)} legitimate URLs")
print()
print("=" * 80)
print("TESTING 50 PHISHING URLs (Expected: PHISHING)")
print("=" * 80)

phishing_correct = 0
phishing_wrong = []
for i, url in enumerate(phishing_urls, 1):
    try:
        r = requests.post(API_URL, json={'url': url}, timeout=10)
        data = r.json()
        result = data.get('result', 'ERROR')
        conf = data.get('confidence', 0)
        if result == 'PHISHING':
            phishing_correct += 1
            status = "OK"
        else:
            status = "WRONG"
            phishing_wrong.append(url[:50])
        print(f"[{i:02d}] {status:<5} {result:<12} {conf:.1%}  {url[:55]}")
    except Exception as e:
        print(f"[{i:02d}] ERROR: {e}")

print()
print("=" * 80)
print("TESTING 50 LEGITIMATE URLs (Expected: LEGITIMATE)")
print("=" * 80)

legit_correct = 0
legit_wrong = []
for i, url in enumerate(legit_urls, 1):
    try:
        r = requests.post(API_URL, json={'url': url}, timeout=10)
        data = r.json()
        result = data.get('result', 'ERROR')
        conf = data.get('confidence', 0)
        if result == 'LEGITIMATE':
            legit_correct += 1
            status = "OK"
        else:
            status = "WRONG"
            legit_wrong.append(url[:50])
        print(f"[{i:02d}] {status:<5} {result:<12} {conf:.1%}  {url[:55]}")
    except Exception as e:
        print(f"[{i:02d}] ERROR: {e}")

print()
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Phishing URLs correctly identified:   {phishing_correct}/50 ({phishing_correct*2}%)")
print(f"Legitimate URLs correctly identified: {legit_correct}/50 ({legit_correct*2}%)")
total = phishing_correct + legit_correct
print(f"Overall Accuracy:                     {total}/100 ({total}%)")
print()
print(f"False Negatives (Phishing marked Legit): {50 - phishing_correct}")
print(f"False Positives (Legit marked Phishing): {50 - legit_correct}")
print("=" * 80)
