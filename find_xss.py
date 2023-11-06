from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


def find_xss_vulnerability(url):
    payloads = ['<script>alert("XSS")</script>', '<img src="men" onerror={alert()}>']

    edge_options = Options()
    edge_options.use_chromium = True
    edge_options.add_argument("--headless")
    driver = webdriver.Edge(options=edge_options)
    driver.set_page_load_timeout(5) 

    try:
        for payload in payloads:
            driver.get(url)
            forms = driver.find_elements(By.TAG_NAME, "form")

            for form in forms:
                print("Testing form..")
                inputs = form.find_elements(By.TAG_NAME, "input")
                textareas = form.find_elements(By.TAG_NAME, "textarea")

                for input_tag in inputs:
                    input_type = input_tag.get_attribute("type")
                    if input_type == "text":
                        input_tag.send_keys(payload)

                for textarea in textareas:
                    textarea.send_keys(payload)

                try:
                    submit_button = form.find_element(
                        By.XPATH,
                        ".//input[@type='submit'] | .//button[@type='submit'] | .//button",
                    )
                    submit_button.click()
                except NoSuchElementException:
                    inputs[-1].send_keys(Keys.RETURN)

                if payload in driver.page_source:
                    print(f"Potential XSS vulnerability found in form at {url}")
                    driver.quit()
                    return True
    except TimeoutException:
        print(f"One of the pages timed out. Maybe they don't like me :(...")
        driver.quit()
        return False
    except Exception as e:
        print(f"An error occurred during testing so browsing was cancelled")
        driver.quit()
        return False

    driver.quit()
    return False
