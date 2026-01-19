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
    special_chars = ['@', '?', '-', '=', '_', '%', '&', '!', '+', '*']
    return sum(url.count(char) for char in special_chars)

def has_https(url):
    return 1 if url.lower().startswith("https") else 0

def suspicious_words_count(url):
    suspicious = [
        'login', 'secure', 'account', 'verify', 'update', 'banking', 
        'confirm', 'password', 'signin', 'credential', 'suspend',
        'unusual', 'confirm', 'authenticate', 'wallet', 'recover',
        'unlock', 'alert', 'notification', 'security', 'urgent'
    ]
    url_lower = url.lower()
    return sum(1 for word in suspicious if word in url_lower)

def has_at_symbol(url):
    return 1 if '@' in url else 0

def has_double_slash_redirect(url):
    try:
        path = urlparse(url).path
        return 1 if '//' in path else 0
    except:
        return 0

def has_hyphen_in_domain(url):
    try:
        hostname = urlparse(url).netloc
        return 1 if '-' in hostname else 0
    except:
        return 0

def get_path_length(url):
    try:
        return len(urlparse(url).path)
    except:
        return 0

def count_query_params(url):
    try:
        query = urlparse(url).query
        if not query:
            return 0
        return query.count('=')
    except:
        return 0

def has_suspicious_tld(url):
    suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work', '.click', '.link', '.info']
    url_lower = url.lower()
    for tld in suspicious_tlds:
        if tld in url_lower:
            return 1
    return 0

def domain_token_count(url):
    try:
        hostname = urlparse(url).netloc
        tokens = re.split(r'[.\-]', hostname)
        return len([t for t in tokens if t])
    except:
        return 0

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
        suspicious_words_count(url),
        has_at_symbol(url),
        has_double_slash_redirect(url),
        has_hyphen_in_domain(url),
        get_path_length(url),
        count_query_params(url),
        has_suspicious_tld(url),
        domain_token_count(url)
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
        'sus_words_count',
        'has_at_symbol',
        'has_double_slash',
        'has_hyphen_domain',
        'path_length',
        'query_param_count',
        'has_sus_tld',
        'domain_token_count'
    ]