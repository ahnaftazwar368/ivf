import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

main_url = input("Please enter URL: ")

visited_urls = set()
urls_to_visit = [main_url]


while urls_to_visit and len(visited_urls) < 10:
    current_url = urls_to_visit.pop(0)
    
    if current_url in visited_urls:
        continue

    print(f"Found page: {current_url}")
    visited_urls.add(current_url)

    try:
        response = requests.get(current_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch {current_url}: {e}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')

    for link in soup.find_all('a', href=True):
        new_url = urljoin(current_url, link['href'])
        if new_url not in visited_urls:
            urls_to_visit.append(new_url)

