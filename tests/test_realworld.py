import requests

API_URL = 'http://127.0.0.1:5000/predict'

print("=" * 90)
print("TESTING REAL-WORLD URLs (NOT from training dataset)")
print("=" * 90)

legitimate_urls = [
    ("https://www.google.com", "Google"),
    ("https://www.facebook.com", "Facebook"),
    ("https://www.amazon.com", "Amazon"),
    ("https://www.github.com", "GitHub"),
    ("https://www.stackoverflow.com", "StackOverflow"),
    ("https://www.reddit.com", "Reddit"),
    ("https://www.wikipedia.org", "Wikipedia"),
    ("https://www.linkedin.com", "LinkedIn"),
    ("https://www.twitter.com", "Twitter/X"),
    ("https://www.netflix.com", "Netflix"),
    ("https://www.spotify.com", "Spotify"),
    ("https://www.paypal.com", "PayPal"),
    ("https://www.ebay.com", "eBay"),
    ("https://www.apple.com", "Apple"),
    ("https://www.microsoft.com", "Microsoft"),
]

suspicious_urls = [
    ("http://192.168.1.100/login.php", "IP-based login"),
    ("http://amaz0n-secure-login.tk/verify", "Fake Amazon"),
    ("http://paypa1-security.ml/update-account", "Fake PayPal"),
    ("http://login.facebook.com.suspicious.xyz/auth", "Fake Facebook"),
    ("http://secure-banking-update.cf/verify.php", "Fake Banking"),
    ("http://microsoft-support.gq/download.exe", "Fake Microsoft"),
    ("http://free-iphone-winner.click/claim", "Scam Prize"),
    ("http://your-account-suspended.info/reactivate", "Account Scam"),
    ("http://urgent-security-alert.top/verify", "Urgency Scam"),
    ("http://netflix-billing-update.work/payment", "Fake Netflix"),
    ("https://docs.google.com/forms/d/e/fake123/viewform", "Google Docs Phishing"),
    ("http://apple-id-verify.ga/confirm", "Fake Apple"),
    ("http://dropbox-share.cf/file/download", "Fake Dropbox"),
    ("http://linkedin-verify.tk/security", "Fake LinkedIn"),
    ("http://update-your-password.xyz/reset", "Password Reset Scam"),
]

print("\n" + "-" * 90)
print("LEGITIMATE SITES (Expected: LEGITIMATE)")
print("-" * 90)

legit_correct = 0
for url, name in legitimate_urls:
    try:
        r = requests.post(API_URL, json={'url': url}, timeout=10)
        data = r.json()
        result = data.get('result', 'ERROR')
        conf = data.get('confidence', 0)
        phish_score = data.get('phishing_score', 0)
        match = "OK" if result == "LEGITIMATE" else "WRONG"
        if result == "LEGITIMATE":
            legit_correct += 1
        print(f"{match:<5} {result:<12} conf:{conf:.1%} phish:{phish_score:.1%}  {name:<15} {url}")
    except Exception as e:
        print(f"ERROR: {name} - {e}")

print("\n" + "-" * 90)
print("SUSPICIOUS/PHISHING URLs (Expected: PHISHING)")
print("-" * 90)

phish_correct = 0
for url, name in suspicious_urls:
    try:
        r = requests.post(API_URL, json={'url': url}, timeout=10)
        data = r.json()
        result = data.get('result', 'ERROR')
        conf = data.get('confidence', 0)
        phish_score = data.get('phishing_score', 0)
        match = "OK" if result == "PHISHING" else "WRONG"
        if result == "PHISHING":
            phish_correct += 1
        print(f"{match:<5} {result:<12} conf:{conf:.1%} phish:{phish_score:.1%}  {name:<20} {url[:50]}")
    except Exception as e:
        print(f"ERROR: {name} - {e}")

print("\n" + "=" * 90)
print("SUMMARY")
print("=" * 90)
print(f"Legitimate correctly identified: {legit_correct}/{len(legitimate_urls)}")
print(f"Phishing correctly identified:   {phish_correct}/{len(suspicious_urls)}")
total = legit_correct + phish_correct
total_urls = len(legitimate_urls) + len(suspicious_urls)
print(f"Overall Accuracy: {total}/{total_urls} ({total*100//total_urls}%)")
print("=" * 90)
