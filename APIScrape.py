import requests
import pandas as pd
import re

# Read ASINs from a file (ONE ASIN PER LINE)
def read_asins(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def clean_title(title):
    return re.sub(r'^\d+(\.\d+)? out of \d+(\.\d+)? stars[\s\-]*', '', title).strip() #removes "#.# out of 5.0 stars" from title issue


def fetch_reviews(asin, pages=1):
    all_reviews = []
    for page in range(1, pages + 1):  # Iterate through specified number of pages
        payload = {
            "source": "amazon_reviews",
            "query": asin,
            "pages": 1,
            "start_page": page,
            "parse": True
        }
        
        response = requests.post(
            "https://realtime.oxylabs.io/v1/queries",
            auth=("User", "Password"),  # Replace with actual credentials
            json=payload
        )
        
        if response.status_code == 200:
            try:
                reviews = response.json()["results"][0]["content"].get("reviews", [])
                for review in reviews:
                    if "title" in review:
                        review["title"] = clean_title(review["title"])
                all_reviews.extend(reviews)
            except (KeyError, IndexError):
                print(f"Warning: Unexpected response format for ASIN {asin} on page {page}")
        else:
            print(f"Error: Failed to fetch reviews for ASIN {asin} (HTTP {response.status_code})")
    
    return all_reviews

def main():
    asins = read_asins("asins.txt")  # Update filename as needed
    all_data = []
    
    for asin in asins:
        print(f"Fetching reviews for ASIN: {asin}")
        reviews = fetch_reviews(asin, pages=2)  # Change number of pages as needed
        for review in reviews:
            review["asin"] = asin  # Add ASIN for reference
        all_data.extend(reviews)
    
    # Save to CSV
    df = pd.DataFrame(all_data)
    df.to_csv("reviews_API.csv", index=False)
    print("Reviews saved to reviews_API.csv")

if __name__ == "__main__":
    main()
