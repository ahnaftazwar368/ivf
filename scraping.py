from bs4 import BeautifulSoup
from urllib.parse import urljoin
from find_xss import find_xss_vulnerability
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options


def get_page(url):
    edge_options = Options()
    edge_options.use_chromium = True
    edge_options.add_argument("--headless")

    driver = webdriver.Edge(options=edge_options)
    driver.get(url)

    page_source = driver.page_source

    driver.quit()
    return page_source


def find_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for link in soup.find_all("a", href=True):
        # if base_url in link:
        new_url = urljoin(base_url, link["href"])
        links.append(new_url)
    return links


def scrape_page(main_url, max_pages=10):
    visited_urls = set()
    urls_to_visit = [main_url]
    xss_found = False
    
    print("Searching for XSS vulnerabilities... plz be patient, I am slow :')...")

    while urls_to_visit and len(visited_urls) < max_pages:
        current_url = urls_to_visit.pop(0)

        if current_url in visited_urls:
            continue

        # print(f"Searching page: {current_url}")
        visited_urls.add(current_url)

        html = get_page(current_url)
        if html:
            new_links = find_links(html, current_url)
            # print("number of urls found: ", len(urls_to_visit))
            urls_to_visit.extend(new_links)
        
        if find_xss_vulnerability(current_url) == True:
            xss_found = True
    
    if not xss_found:
        print("No XSS vulnerabilities found")