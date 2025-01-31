import subprocess
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Remote
import chromedriver_autoinstaller
import re
import os



TEST_URL = "http://localhost:3000/materialType"

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # This means you won't see the actual icon
    chrome_options.add_argument("--disable-gpu") # Disable GPU acceleration (required in headless mode)
    chrome_options.add_argument("--no-sandbox")  # Might help in some environments
    # This will change depending on your driver
    if os.getenv("CI"):  # If in CI environment
        # Automatically installs the correct ChromeDriver version for your installed Chrome
        chromedriver_autoinstaller.install()
        driver = webdriver.Chrome(options=chrome_options)

    else:
        path = '/Users/l_filippelli/Downloads/chromedriver-mac-x64/chromedriver'

        driver = webdriver.Chrome(service=Service(path), options=chrome_options)

    yield driver
    driver.quit()

def test_navbar(driver):
    driver.get(TEST_URL)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "nav")))

    # Find the header row
    header_row = driver.find_element(By.CSS_SELECTOR, "ul")

    # Get the full text of the header row (all titles in one string)
    header_text = header_row.text
    print(header_text)

    #TODO account for user difference in nav bar once we render properly

    assert header_text == "Inventory\nUsers\nMaterial Type" or header_text == "Inventory\nMaterial Type"

