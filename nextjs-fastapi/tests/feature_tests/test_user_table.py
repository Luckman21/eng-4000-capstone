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



TEST_URL = "http://127.0.0.1:3000/users"

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # This means you won't see the actual icon
    chrome_options.add_argument("--disable-gpu") # Disable GPU acceleration (required in headless mode)
    chrome_options.add_argument("--no-sandbox")  # Might help in some environments
    # This will change depending on your driver

    # Automatically installs the correct ChromeDriver version for your installed Chrome
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=chrome_options)

    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def login(driver):
    log_super_admin_in(driver)
    time.sleep(3)



def test_user_table_header(driver, login):
    driver.get(TEST_URL)
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
    rows = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr"))
    )

    # Find the header row
    header_row = driver.find_element(By.CSS_SELECTOR, "thead tr")

    # Get the full text of the header row (all titles in one string)
    header_text = header_row.text

    assert header_text == "ID USERNAME EMAIL USER TYPE ACTIONS" or header_text == "ID USERNAME EMAIL USER TYPE"

def test_user_table_buttons(driver, login):
    driver.get(TEST_URL)
    rows = WebDriverWait(driver, 30).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "tbody tr"))
    )

    rows = driver.find_elements(By.CLASS_NAME, "relative flex items-center gap-2")

    # Check each row for the presence of two SVG elements
    for index, row in enumerate(rows):
        WebDriverWait(row, 120).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "svg")))
        svg_elements = row.find_elements(By.TAG_NAME, "svg")

        # Assert that each row has exactly 2 SVGs (or adjust as necessary)
        assert len(svg_elements) == 2, f"Row {index + 1} does not have exactly 2 SVG elements."


def test_user_table_order(driver, login):
    driver.get(TEST_URL)
    WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.XPATH, "//tbody/tr[1]/td[1]")))
    WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.XPATH, "//tbody/tr[2]/td[1]")))

    first_td = driver.find_element(By.XPATH, "//tbody/tr[1]/td[1]")
    assert first_td.text == '1'

    second_td = driver.find_element(By.XPATH, "//tbody/tr[2]/td[1]")
    assert second_td.text == '2'


def test_edit_button(driver, login):

    driver.get(TEST_URL)
    WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.XPATH, "//tbody/tr[1]/td[5]")))

    button = driver.find_element(By.XPATH, "//tbody/tr[1]/td[5]/div/span[1]")
    button.click()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, "section")))

    panel = driver.find_element(By.TAG_NAME, "section")

    header = panel.find_element(By.CSS_SELECTOR, "header")

    assert header.text == "Edit User"

    labels = panel.find_elements(By.CSS_SELECTOR, "label")

    assert labels[0].text == "Username"
    assert labels[1].text == "Email"
    assert labels[2].text == "User Type"

def test_create_button(driver, login):
    driver.get(TEST_URL)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button")))

    buttons = driver.find_elements(By.CSS_SELECTOR, "button")
    button = buttons[0]
    button.click()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, "section")))

    panel = driver.find_element(By.CSS_SELECTOR, "section")

    header = panel.find_element(By.CSS_SELECTOR, "header")

    assert header.text == "Add New User"

    edit_fields = panel.find_element(By.CSS_SELECTOR, "div")

    labels = panel.find_elements(By.CSS_SELECTOR, "label")

    assert labels[0].text == "Username"
    assert labels[1].text == "Password"
    assert labels[2].text == "Email"
    assert labels[3].text == "User Type"


def test_delete_confirmation(driver, login):
    driver.get(TEST_URL)
    WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.XPATH, "//tbody/tr[1]/td[5]")))

    button = driver.find_element(By.XPATH, "//tbody/tr[1]/td[5]/div/span[2]")
    button.click()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, "section")))

    popup = driver.find_element(By.TAG_NAME, "section")

    header = popup.find_element(By.TAG_NAME, "header")
    assert header.text == "Delete Item"

    text = popup.find_element(By.XPATH, "div[2]")
    assert text.text == 'Are you sure you want to delete this item? This action cannot be undone.'

    footer = popup.find_element(By.CSS_SELECTOR, "footer")

    buttons = footer.find_elements(By.CSS_SELECTOR, "button")

    assert len(buttons) == 2

# TODO: Make test to assess status once material migration is complete