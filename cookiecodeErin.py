import requests
from bs4 import BeautifulSoup

# Replace with your cookies after logging in manually
cookies = {
    'session-id': 'your-session-id',
    'session-id-time': 'your-session-id-time',
    'ubid-main': 'your-ubid-main',
    # add other cookies from your browser here
}

custom_headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "Gecko/20100101 Firefox/135.0"
    ),
}

def get_soup(url):
    response = requests.get(url, headers=custom_headers, cookies=cookies)
    if response.status_code != 200:
        print("Error in getting webpage")
        exit(-1)
    return BeautifulSoup(response.text, "lxml")

# The rest of the code remains the same
