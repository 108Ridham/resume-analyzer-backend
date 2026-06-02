import os
import re
from collections import Counter
from app.services.ats_checker import TECHNICAL_AND_LEADERSHIP_KEYWORDS

def get_embedding(text: str):
    # Construct a keyword-based frequency vector based on our whitelist.
    # This runs 100% offline, consumes 0 extra memory, and has no network requirements.
    text_lower = text.lower()
    tokens = re.findall(r'\b[a-zA-Z0-9\+\#\-\.]+\b', text_lower)
    counts = Counter(tokens)
    
    vector = []
    for keyword in TECHNICAL_AND_LEADERSHIP_KEYWORDS:
        # Check frequency of keyword
        if " " in keyword:
            vector.append(float(text_lower.count(keyword)))
        else:
            vector.append(float(counts.get(keyword, 0)))
            
    return vector