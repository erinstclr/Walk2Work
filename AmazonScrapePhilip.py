import requests
from bs4 import BeautifulSoup
import pandas as pd

custom_headers = {
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "Gecko/20100101 Firefox/135.0"
    )
}

def get_soup(url):
    response = requests.get(url, headers=custom_headers)

    if response.status_code != 200:
        print("Error in getting webpage")
        exit(-1)

    return BeautifulSoup(response.text, "lxml")

def extract_review(review, is_local=True):
    author = review.select_one(".a-profile-name").text.strip()
    rating = (
        review.select_one(".review-rating > span").text
        .replace("out of 5 stars", "")
        .strip()
    )
    date = review.select_one(".review-date").text.strip()
    
    if is_local:
        title = (
            review.select_one(".review-title")
            .select_one("span:not([class])")
            .text.strip()
        )
        content = ' '.join(
            review.select_one(".review-text").stripped_strings
        )
        img_selector = ".review-image-tile"
    else:
        title = (
            review.select_one(".review-title")
            .select_one(".cr-original-review-content")
            .text.strip()
        )
        content = ' '.join(
            review.select_one(".review-text")
            .select_one(".cr-original-review-content")
            .stripped_strings
        )
        img_selector = ".linkless-review-image-tile"
    
    verified_element = review.select_one("span.a-size-mini")
    verified = verified_element.text.strip() if verified_element else None

    image_elements = review.select(img_selector)
    images = (
        [img.attrs["data-src"] for img in image_elements] 
        if image_elements else None
    )

    return {
        "type": "local" if is_local else "global",
        "author": author,
        "rating": rating,
        "title": title,
        "content": content.replace("Read more", ""),
        "date": date,
        "verified": verified,
        "images": images
    }

def get_reviews(soup):
    reviews = []
    
    # Get both local and global reviews using the same function.
    local_reviews = soup.select("#cm-cr-dp-review-list > li")
    global_reviews = soup.select("#cm-cr-global-review-list > li")
    
    for review in local_reviews:
        reviews.append(extract_review(review, is_local=True))
    
    for review in global_reviews:
        reviews.append(extract_review(review, is_local=False))
    
    return reviews

def process_ids_from_file(filename):
    try:
        with open(filename, 'r') as file:
            for line in file:
                asin_str = line.strip()
                if asin_str:
                    process_id(asin_str)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_id(asin_str):
    search_url = f"https://www.amazon.com/dp/{asin_str}"
    soup = get_soup(search_url)
    reviews = get_reviews(soup)
    
    df = pd.DataFrame(reviews)
    df.to_csv(f"reviews_{asin_str}.csv", index=False)

if __name__ == "__main__":
    file_path = "ids.txt"  # Change this to your actual file path
    process_ids_from_file(file_path)
