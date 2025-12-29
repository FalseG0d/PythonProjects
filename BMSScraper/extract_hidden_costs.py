# extract_hidden_costs.py
import re

KEYWORDS = [
    "extra", "additional", "charged", "not included",
    "pay at venue", "firing", "clay", "frame"
]

def extract_hidden_costs(description):
    hits = []
    for kw in KEYWORDS:
        if re.search(kw, description, re.IGNORECASE):
            hits.append(kw)
    return ", ".join(hits) if hits else None