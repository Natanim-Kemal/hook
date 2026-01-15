import re
from urllib.parse import urlparse
import math

def calculate_entropy(text):
    if not text:
        return 0
    entropy = 0
    for x in range(256):
        p_x = float(text.count(chr(x))) / len(text)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy

def has_ip_address(url):
    match = re.search(
        r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\/)|'
        r'((0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\/)'
        r'(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)
    return 1 if match else 0

def get_url_length(url):
    return len(url)

def get_hostname_length(url):
    try:
        return len(urlparse(url).netloc)
    except:
        return 0

def count_dots(url):
    return url.count('.')

def count_subdomains(url):
    try:
        hostname = urlparse(url).netloc
        if not hostname:
            return 0
        return hostname.count('.')
    except:
        return 0

def count_slashes(url):
    return url.count('/')

def count_digits(url):
    return sum(c.isdigit() for c in url)

def count_special_chars(url):
    special_chars = ['@', '?', '-', '=', '_', '%']
    return sum(url.count(char) for char in special_chars)

def has_https(url):
    return 1 if "https" in url else 0

def suspicious_words_count(url):
    suspicious = ['login', 'secure', 'account', 'verify', 'update', 'banking', 'confirm']
    return sum(1 for word in suspicious if word in url.lower())

def extract_features(url):
    return [
        has_ip_address(url),
        get_url_length(url),
        get_hostname_length(url),
        count_dots(url),
        count_subdomains(url),
        count_slashes(url),
        count_digits(url),
        count_special_chars(url),
        calculate_entropy(url),
        has_https(url),
        suspicious_words_count(url)
    ]

def get_feature_names():
    return [
        'has_ip',
        'url_len',
        'hostname_len',
        'dot_count',
        'subdomain_count',
        'slash_count',
        'digit_count',
        'special_char_count',
        'entropy',
        'has_https',
        'sus_words_count'
    ]
