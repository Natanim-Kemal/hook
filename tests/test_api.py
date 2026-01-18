import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestAPIEndpoints:
    
    def test_feature_extraction_import(self):
        from feature_extraction import extract_features, get_feature_names
        assert callable(extract_features)
        assert callable(get_feature_names)
    
    def test_feature_names_count(self):
        from feature_extraction import get_feature_names
        feature_names = get_feature_names()
        assert len(feature_names) == 18
    
    def test_extract_features_basic(self):
        from feature_extraction import extract_features
        url = "https://www.google.com"
        features = extract_features(url)
        assert len(features) == 18
        assert all(isinstance(f, (int, float)) for f in features)
    
    def test_extract_features_phishing_indicators(self):
        from feature_extraction import extract_features
        phishing_url = "http://192.168.1.1/login/secure/verify/account.html?user=admin"
        features = extract_features(phishing_url)
        assert len(features) == 18
    
    def test_extract_features_with_special_chars(self):
        from feature_extraction import extract_features
        url = "https://example.com/path?param1=value1&param2=value2"
        features = extract_features(url)
        assert len(features) == 18
    
    def test_https_detection(self):
        from feature_extraction import has_https
        assert has_https("https://secure.com") == 1
        assert has_https("http://insecure.com") == 0
    
    def test_ip_address_detection(self):
        from feature_extraction import has_ip_address
        assert has_ip_address("http://192.168.1.1/path") == 1
        assert has_ip_address("https://google.com") == 0
    
    def test_suspicious_words_count(self):
        from feature_extraction import suspicious_words_count
        assert suspicious_words_count("http://example.com/login") >= 1
        assert suspicious_words_count("http://example.com/about") == 0
    
    def test_url_length_calculation(self):
        from feature_extraction import get_url_length
        url = "https://example.com"
        assert get_url_length(url) == len(url)


class TestEdgeCases:
    
    def test_empty_url(self):
        from feature_extraction import extract_features
        features = extract_features("")
        assert len(features) == 18
    
    def test_malformed_url(self):
        from feature_extraction import extract_features
        features = extract_features("not-a-valid-url")
        assert len(features) == 18


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
