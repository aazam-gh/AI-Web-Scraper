from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # Or other browser options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

AUTH = 'brd-customer-hl_6f1e6d0c-zone-major_scrapper:9d2148keprop'
SBR_WEBDRIVER = f'https://{AUTH}@zproxy.lum-superproxy.io:9515'


def scrape_website(website):
    print("Connecting with Selenium...")
    try:
        options = Options()
        # Add any Chrome options you need (headless, etc.)
        # Example for headless mode:
        options.add_argument("--headless")  # Run Chrome in headless mode

        driver = webdriver.Chrome(options=options) # Or other browser driver (Firefox, Edge, etc.)
        driver.get(website)

        # Handle Captchas (this is still a complex issue)
        # You might need to add explicit waits and checks for captcha elements
        # Example (you would need to adapt this to the specific captcha):
        # try:
        #     captcha_element = WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.ID, "captcha-element-id")) # Replace with the actual ID
        #     )
        #     print("Captcha detected. Please solve it manually in the browser.")
        #     input("Press Enter to continue after solving captcha...") # Pause execution
        # except:
        #     print("No captcha detected (or timed out).")

        print("Navigated! Scraping page content...")
        html = driver.page_source
        driver.quit()  # Close the browser when done
        return html
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=9000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
    
