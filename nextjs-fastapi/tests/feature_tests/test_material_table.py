import subprocess
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():

    chrome_options = Options()
    chrome_options.add_argument("--headless") # This means you won't see the actual icon
    chrome_options.add_argument("--disable-gpu")

    # This will change depending on your driver
    path = '/Users/l_filippelli/Downloads/chromedriver-mac-x64/chromedriver'
    driver = webdriver.Chrome(service=Service(path), options=chrome_options)
    yield driver
    driver.quit()

def test_material_table_header(driver):
    driver.get("http://localhost:3000")
    time.sleep(3)

    # ID Header
    element = driver.find_element(By.ID, "react-aria-:R2fj6:-id")
    assert element.text == "ID"

    # Colour Header
    element = driver.find_element(By.ID, "react-aria-:R2fj6:-colour")
    assert element.text == "COLOUR"

    # Name Header
    element = driver.find_element(By.ID, "react-aria-:R2fj6:-name")
    assert element.text == "NAME"

    # Weight Header
    element = driver.find_element(By.ID, "react-aria-:R2fj6:-mass")
    assert element.text == "Weight (g)"

    # Status Header
    element = driver.find_element(By.ID, "react-aria-:R2fj6:-status")
    assert element.text == "STATUS"

    # Actions Header
    element = driver.find_element(By.ID, "react-aria-:R2fj6:-actions")
    assert element.text == "ACTIONS"


def test_material_table_buttons(driver):

    driver.get("http://localhost:3000")
    time.sleep(3)

    # Locate all rows in the table
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "react-aria-:R2fj6:"))
    )

    rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")

    # Check each row for the presence of two SVG elements
    for index, row in enumerate(rows):
        svg_elements = row.find_elements(By.TAG_NAME, "svg")

        # Assert that each row has exactly 2 SVGs (or adjust as necessary)
        assert len(svg_elements) == 2, f"Row {index + 1} does not have exactly 2 SVG elements."

def test_material_table_order(driver):

    driver.get("http://localhost:3000")
    time.sleep(3)

    # Locate all rows in the table
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "react-aria-:R2fj6:"))
    )

    first_td = table.find_element(By.XPATH, "//tbody/tr[1]/td[1]")
    assert first_td.text == '1'

    second_td = table.find_element(By.XPATH, "//tbody/tr[2]/td[1]")
    assert second_td.text == '2'

# TODO: Make test to assess status once material migration is complete