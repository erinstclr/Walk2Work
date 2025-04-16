import pandas as pd
import gender_guesser.detector as gender
import re
import sys

# Initialize gender detector
d = gender.Detector(case_sensitive=False)

# Define features and their associated keywords
feature_keywords = {
    "assembly": ["assembly", "assemble", "setup", "put together", "installation", "build", "construct", "install", "set up", "piece together", "easy to assemble", "complex assembly", "assemble time"],
    "noise": ["noise", "quiet", "loud", "silent", "noisy", "sound", "whisper", "hum", "buzz", "clatter", "rattle", "muted", "volume"],
    "width": ["wide", "narrow", "width", "broad", "slim", "spacious", "tight", "roomy", "cramped", "breadth", "space"],
    "speed": ["speed", "fast", "slow", "quick", "rapid", "sluggish", "swift", "pace", "performance", "responsiveness", "laggy", "brisk"],
    "quality": ["quality", "durable", "sturdy", "cheap", "flimsy", "well-made", "robust", "poorly made", "reliable", "fragile", "build quality", "craftsmanship", "solid", "shoddy"],
    "portability": ["move", "carry", "portable", "lightweight", "heavy", "mobile", "transportable", "cumbersome", "easy to move", "portability", "maneuverable", "bulky"],
    "size": ["small", "big", "compact", "size", "large", "tiny", "bulky", "space-saving", "oversized", "petite", "dimensions", "fit", "roomy"],
    "customer service": ["seller", "customer service", "support", "responded", "helpful", "unresponsive", "contact", "assistance", "service", "helpdesk", "response time", "support team", "vendor"],
    "convenience": ["convenient", "easy to use", "accessible", "ready", "handy", "streamlined", "practical", "hassle-free", "user-friendly", "effortless", "simple to use", "time-saving", "functional"],
    "usability": ["user-friendly", "intuitive", "clear", "simple", "navigation", "interface", "straightforward", "easy to operate", "complicated", "ease of use", "accessible", "logical", "confusing"]
}

positive_keywords = [
    "easy", "great", "good", "love", "quiet", "responded", "promptly", "no assembly", "smooth", "super",
    "excellent", "fantastic", "awesome", "wonderful", "perfect", "amazing", "reliable", "impressive",
    "solid", "happy", "satisfied", "well-made", "convenient", "efficient", "comfortable", "durable",
    "fast", "beautiful", "high-quality", "affordable", "user-friendly", "versatile", "sturdy",
    "recommended", "pleased", "seamless", "outstanding", "intuitive", "value", "quick"
]

negative_keywords = [
    "bad", "hard", "difficult", "narrow", "slow", "loud", "problem", "cheap", "flimsy", "noisy",
    "poor", "broken", "defective", "unreliable", "disappointed", "frustrating", "complicated",
    "uncomfortable", "weak", "faulty", "terrible", "useless", "overpriced", "damaged", "confusing",
    "low-quality", "short-lived", "annoying", "unstable", "inconvenient", "waste", "malfunction",
    "unresponsive", "crappy", "awkward", "inferior", "regret", "failure"
]

desired_keywords = [
    "wish", "would like", "hope for", "desired", "would be nice", "want", "looking for", "missing",
    "lack", "could use", "need", "should have", "if only", "better if", "wanted", "hoped",
    "preferably", "could improve", "suggest", "more", "less", "instead", "ideally"
]

neutral_keywords = [
    "okay", "average", "normal", "standard", "typical", "fine", "decent", "moderate", "basic",
    "functional", "works", "acceptable", "sufficient", "regular", "simple", "plain", "adequate",
    "expected", "fair", "middle"
]

# List of desired features (what users wish the product had)
missing_features_keywords = {
    "handle": ["handle", "grip", "carrying", "bar", "lift"],
    "Bluetooth": ["bluetooth", "wireless", "connection", "sync"],
    "remote": ["remote", "controller", "app control"],
    "wheels": ["wheels", "roll", "casters", "transport"],
    "foldability": ["fold", "compact", "space-saving", "store easily"],
    "quiet": ["quiet", "silent", "noise-free", "low noise"],
    "shock absorption": ["shock absorption", "cushioning", "impact protection"],
    "adjustable speed": ["adjustable speed", "variable speed", "speed control"],
    "heart rate monitor": ["heart rate monitor", "pulse monitor", "fitness tracker"],
    "display screen": ["display", "screen", "monitor", "LCD"],
    "USB charging port": ["USB", "charge", "charging port"],
    "LED lighting": ["LED", "lighting", "light", "backlight"],
    "desk compatibility": ["desk", "adjustable desk", "compatible desk", "desk size"]
}

# Regular expression pattern to detect age mentions
age_pattern = r"(?:\b(?:I am|I'm|age)\s*(\d{1,2})\s*(?:years? old|y/o|years old)\b|(?:over|above|at)\s*(\d{1,2})\s*(?:\+|\s*years?)\b)"

def guess_gender(name):
    if not name or not isinstance(name, str):
        return "U"
    first_name = name.split()[0].title()  # Normalize to title case
    result = d.get_gender(first_name)
    if result in ("male", "mostly_male"):
        return "M"
    elif result in ("female", "mostly_female"):
        return "F"
    else:
        return "U"

def extract_age(text):
    if not isinstance(text, str):
        return None
    match = re.search(age_pattern, text, re.IGNORECASE)
    if match:
        # Return the first non-None group (either exact age or over age)
        return match.group(1) or match.group(2)
    return None

def analyze_features(text):
    if not isinstance(text, str):
        text = ""
    text = text.lower()
    result = {}
    
    # Analyze feature sentiments
    for feature, keywords in feature_keywords.items():
        if any(kw in text for kw in keywords):
            has_positive = any(pk in text for pk in positive_keywords)
            has_negative = any(nk in text for nk in negative_keywords)
            has_neutral = any(nuk in text for nuk in neutral_keywords)
            
            if has_positive:
                sentiment = "positive"
            elif has_negative:
                sentiment = "negative"
            elif has_neutral:
                sentiment = "neutral"
            else:
                sentiment = "neutral"
            result[feature] = sentiment
        else:
            result[feature] = "N/A"
    
    # Check for missing or wished features
    wished_features = []
    for feature, keywords in missing_features_keywords.items():
        if any(kw in text for kw in keywords) and any(dk in text for dk in desired_keywords):
            wished_features.append(feature)
    
    result["wished_features"] = ", ".join(wished_features) if wished_features else ""
    
    return result

# Load data with error handling
try:
    df = pd.read_csv("reviews_API.csv")
except FileNotFoundError:
    print("Error: 'reviews_API.csv' not found. Please ensure the file exists in the working directory.")
    sys.exit(1)
except pd.errors.EmptyDataError:
    print("Error: 'reviews_API.csv' is empty.")
    sys.exit(1)
except Exception as e:
    print(f"Error loading 'reviews_API.csv': {e}")
    sys.exit(1)

# Processed output
processed_rows = []

for _, row in df.iterrows():
    author = row.get("author", "")
    content = row.get("content", "")
    rating = row.get("rating", None)
    asin = row.get("asin", "")

    gender = guess_gender(author)
    age = extract_age(content)
    feature_sentiments = analyze_features(content)

    processed_row = {
        "asin": asin,
        "author": author,
        "gender": gender,
        "age": age,
        "rating": rating,
        "content": content,
    }

    # Add feature sentiments and wished features
    processed_row.update(feature_sentiments)

    processed_rows.append(processed_row)

# Output to CSV
try:
    output_df = pd.DataFrame(processed_rows)
    output_df.to_csv("structured_reviews.csv", index=False)
    print("✅ Done! Structured review data saved to 'structured_reviews.csv'")
except Exception as e:
    print(f"Error saving 'structured_reviews.csv': {e}")
    sys.exit(1)