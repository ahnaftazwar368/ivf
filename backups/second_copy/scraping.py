import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from vulnerability import find_sqli_vulnerability


def get_page(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None


def find_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for link in soup.find_all("a", href=True):
        new_url = urljoin(base_url, link["href"])
        links.append(new_url)
    return links


def scrape_page(main_url, max_pages=5):
    visited_urls = set()
    urls_to_visit = [main_url]
    

    while urls_to_visit and len(visited_urls) < max_pages:
        current_url = urls_to_visit.pop(0)

        if current_url in visited_urls:
            continue

        print(f"Searching page: {current_url}")
        visited_urls.add(current_url)

        html = get_page(current_url)
        if html:
            print(html)
            new_links = find_links(html, current_url)
            print("number of urls found: ", len(urls_to_visit))
            urls_to_visit.extend(new_links)
            
            if find_sqli_vulnerability(current_url, html):
                print(f"Potential SQLi vulnerability found at {current_url}")
                print(f"Ay yo {current_url} is vulnerable, attack him!")
