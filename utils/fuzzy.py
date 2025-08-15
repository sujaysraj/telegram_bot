# utils/fuzzy.py

import difflib

def fuzzy_lookup(name: str, data: dict) -> str | None:
    from rapidfuzz import fuzz

    best_match = None
    best_score = 0

    for key in data:
        score = fuzz.ratio(name.lower(), key.lower())
        print(f"[DEBUG] Matching {name} vs {key}: {score}")
        if score > best_score:
            best_score = score
            best_match = key

    if best_score >= 80:
        return best_match
    return None