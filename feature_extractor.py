import re
from urllib.parse import urlparse

def extract_features(url):
    parsed = urlparse(url)
    domain = parsed.netloc

    suspicious_words = ["login", "verify", "secure", "account", "bank", "paypal", "update", "free", "confirm"]

    return [
        len(url),
        url.count("."),
        url.count("-"),
        url.count("@"),
        url.count("?"),
        url.count("="),
        url.count("%"),
        sum(c.isdigit() for c in url),
        1 if url.startswith("https") else 0,
        1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0,
        len(domain),
        sum(1 for word in suspicious_words if word in url.lower())
    ]