import subprocess
import pytest
import time
from selenium import webdriver
from selenium.common import StaleElementReferenceException
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
from backend.controller.main import get_app
from fastapi.testclient import TestClient

client = TestClient(get_app())

TEST_URL = "http://127.0.0.1:3000/inventory"

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # This means you won't see the actual icon
    chrome_options.add_argument("--disable-gpu") # Disable GPU acceleration (required in headless mode)
    chrome_options.add_argument("--no-sandbox")  # Might help in some environments
    chrome_options.add_argument("--window-size=1920,1080")
    # This will change depending on your driver

    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=chrome_options)

    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def login(driver):
    log_super_admin_in(driver)
    time.sleep(3)


def test_notif_panel(driver, login):
    nav = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.TAG_NAME, "nav")))

    button = driver.find_element(By.XPATH, "//tbody/tr[1]/td[8]/div/span[1]")
    button.click()

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, "section")))

    panel = driver.find_element(By.TAG_NAME, "section")


    labels = panel.find_elements(By.CSS_SELECTOR, "label")
    assert labels[2].text == "Weight (g)"

    # Get buttons (slider stuff at the top)

    buttons = panel.find_elements(By.CSS_SELECTOR, "button")
    remove = buttons[3].find_element(By.CSS_SELECTOR, 'div')
    remove.click()

    WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input')))
    field = panel.find_elements(By.CSS_SELECTOR, 'input')
    field[2].send_keys("490.0")

    update_button = driver.find_element(By.XPATH, "//button[text()='Update Material']")
    update_button.click()
    time.sleep(5)

    WebDriverWait(nav, 40).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg')))
    notif_button = nav.find_element(By.TAG_NAME, 'svg')
    driver.execute_script("arguments[0].scrollIntoView(true);", notif_button)
    notif_button.click()
    time.sleep(3)

    panel = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.TAG_NAME, "section")))
    header = panel.find_element(By.TAG_NAME, "header")
    assert header.text == 'Alerts'

    panel = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.TAG_NAME, "section")))
    titles = panel.find_elements(By.TAG_NAME, "h1")
    assert titles[0].text == 'Low Stock Materials'
    assert titles[1].text == 'Shelf Status'

    notif = panel.find_element(By.XPATH, "(./div//div//div//div)[1]")

    notif_elements = notif.find_elements(By.CSS_SELECTOR, 'p')
    assert notif_elements[0].text == 'Black'
    assert notif_elements[1].text == 'Material ID: 1'
    assert notif_elements[2].text == 'Mass: 10g'

    link = notif.find_element(By.CSS_SELECTOR, 'a')
    name = link.text
    assert 'View Supplier' in name





