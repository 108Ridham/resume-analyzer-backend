import re

def basic_cleaning(text: str) -> str:
    text = text.lower()
    text = text.replace("c++", "cplusplus")          # ✅ protect before cleaning
    text = text.replace("node.js", "node js")        # ✅ normalize
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = text.replace("cplusplus", "c++")          # ✅ restore after cleaning
    return text

def normalise_text(text: str) -> str:
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def preprocess_text(text: str) -> str:
    text = basic_cleaning(text)
    text = normalise_text(text)
    return text