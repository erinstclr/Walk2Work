import pandas as pd
import gender_guesser.detector as gender
import re

# Initialize gender detector
d = gender.Detector()

# Define features and their associated keywords
feature_keywords = {
    "assembly": ["assembly", "assemble", "setup", "put together"],
    "noise": ["noise", "quiet", "loud", "silent"],
    "width": ["wide", "narrow", "width"],
    "speed": ["speed", "fast", "slow"],
    "quality": ["quality", "durable", "sturdy", "cheap", "flimsy"],
    "portability": ["move", "carry", "portable", "lightweight", "heavy"],
    "size": ["small", "big", "compact", "size"],
    "customer service": ["seller", "customer service", "support", "responded"],
    "convenience": ["convenient", "easy to use", "accessible", "ready", "handy", "streamlined"],
    "usability": ["user-friendly", "intuitive", "clear", "simple", "navigation", "interface"]
}

positive_keywords = ["easy", "great", "good", "love", "quiet", "responded", "promptly", "no assembly", "smooth", "super"]
negative_keywords = ["bad", "hard", "difficult", "narrow", "slow", "loud", "problem", "cheap", "flimsy", "noisy"]
desired_keywords = ["wish", "would like", "hope for", "desired", "would be nice", "want", "looking for", "missing", "lack", "could use"]

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

# Regular expression pattern to detect age mentions (including ranges like 65+, over 50)
age_pattern = r"(?:\b(?:I am|I'm|age)\s*(\d{1,2})\s*(?:years? old|y/o|years old)\b|(?:over|above|at)\s*(\d{1,2})\s*(?:\+|\s*years?)\b)"

def guess_gender(name):
    first_name = name.split()[0]
    result = d.get_gender(first_name)
    if result in ("male", "mostly_male"):
        return "M"
    elif result in ("female", "mostly_female"):
        return "F"
    else:
        return "U"

def analyze_features(text):
    text = text.lower()
    result = {}
    for feature, keywords in feature_keywords.items():
        if any(kw in text for kw in keywords):
            sentiment = "positive" if any(pk in text for pk in positive_keywords) else "negative"
            result[feature] = sentiment
        else:
            result[feature] = "N/A"
    
    # Check for missing or wished features
    wished_features = []
    for feature, keywords in missing_features_keywords.items():
        if any(kw in text for kw in keywords) and any(dk in text for dk in desired_keywords):
            wished_features.append(feature)
    
    result["wished_features"] = ", ".join(wished_features) if wished_features else " "
    
    return result

# Load data
df = pd.read_csv("reviews_API.csv")

# Processed output
processed_rows = []

for _, row in df.iterrows():
    author = row["author"]
    gender = guess_gender(author)
    content = row["content"]
    rating = row["rating"]
    asin = row["asin"]


    feature_sentiments = analyze_features(content)

    processed_row = {
        "asin": asin,
        "author": author,
        "gender": gender,
        "rating": rating,
        "content": content,
        
    }

    # Add each feature column to the row
    processed_row.update(feature_sentiments)

    processed_rows.append(processed_row)

# Output to CSV
output_df = pd.DataFrame(processed_rows)
output_df.to_csv("structured_reviews.csv", index=False)
print("✅ Done! Structured review data saved to 'structured_reviews_with_age.csv'")
