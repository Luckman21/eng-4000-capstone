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
from tests.feature_tests.login_helper import log_admin_in, log_super_admin_in



TEST_URL = "http://127.0.0.1:3000/materialType"

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # This means you won't see the actual icon
    chrome_options.add_argument("--disable-gpu") # Disable GPU acceleration (required in headless mode)
    chrome_options.add_argument("--no-sandbox")  # Might help in some environments
    # This will change depending on your driver
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=chrome_options)

    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def login(driver):
    log_admin_in(driver)
    time.sleep(3)

def test_navbar(driver, login):

    driver.get(TEST_URL)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "nav")))

    # Find the header row
    header_row = driver.find_element(By.CSS_SELECTOR, "ul")

    # Get the full text of the header row (all titles in one string)
    header_text = header_row.text
    print(header_text)

    #TODO account for user difference in nav bar once we render properly

    assert header_text == "Inventory\nUsers\nMaterial Type" or header_text == "Inventory\nMaterial Type"

