import subprocess
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

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

    # Find the header row
    header_row = driver.find_element(By.CSS_SELECTOR, "thead tr")

    # Get the full text of the header row (all titles in one string)
    header_text = header_row.text

    assert header_text == "ID COLOUR SUPPLIER LINK MASS (g) MATERIAL TYPE SHELF STATUS ACTIONS"


def test_material_table_buttons(driver):

    driver.get("http://localhost:3000")
    time.sleep(3)


    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

    # Check each row for the presence of two SVG elements
    for index, row in enumerate(rows):
        svg_elements = row.find_elements(By.TAG_NAME, "svg")

        # Assert that each row has exactly 2 SVGs (or adjust as necessary)
        assert len(svg_elements) == 3, f"Row {index + 1} does not have exactly 2 SVG elements."

def test_material_table_order(driver):

    driver.get("http://localhost:3000")
    time.sleep(3)

    first_td = driver.find_element(By.XPATH, "//tbody/tr[1]/td[1]")
    assert first_td.text == '1'

    second_td = driver.find_element(By.XPATH, "//tbody/tr[2]/td[1]")
    assert second_td.text == '2'

def test_edit_button(driver):

    driver.get("http://localhost:3000")
    time.sleep(3)

    button = driver.find_element(By.XPATH, "//tbody/tr[1]/td[8]/div/span[1]")
    button.click()
    time.sleep(2)

    panel = driver.find_element(By.TAG_NAME, "section")

    header = panel.find_element(By.CSS_SELECTOR, "header")

    assert header.text == "Edit Material"

    labels = panel.find_elements(By.CSS_SELECTOR, "label")

    assert labels[0].text == "Supplier Link"
    assert labels[1].text == "Colour"
    assert labels[2].text == "Weight (g)"
    assert labels[3].text == "Shelf"
    assert labels[4].text == "Material Type"

def test_create_button(driver):
    driver.get("http://localhost:3000")
    time.sleep(3)

    buttons = driver.find_elements(By.CSS_SELECTOR, "button")
    button = buttons[0]
    button.click()

    panel = driver.find_element(By.CSS_SELECTOR, "section")

    header = panel.find_element(By.CSS_SELECTOR, "header")

    assert header.text == "Add New Material"

    edit_fields = panel.find_element(By.CSS_SELECTOR, "div")

    labels = panel.find_elements(By.CSS_SELECTOR, "label")

    assert labels[0].text == "Colour"
    assert labels[1].text == "Supplier Link"
    assert labels[2].text == "Weight (g)"
    assert labels[3].text == "Shelf"
    assert labels[4].text == "Material Type"


def test_delete_confirmation(driver):
    driver.get("http://localhost:3000")
    time.sleep(3)

    row = driver.find_elements(By.CSS_SELECTOR, "tbody tr")[0]
    print(row.text)

    delete_icon = row.find_elements(By.TAG_NAME, "svg")[2]

    delete_icon.click()
    time.sleep(3)

    popup = driver.find_element(By.TAG_NAME, "section")

    header = popup.find_element(By.TAG_NAME, "header")
    assert header.text == "Delete Item"

    text = popup.find_element(By.XPATH, "div[2]")
    assert text.text == 'Are you sure you want to delete this item? This action cannot be undone.'

    footer = popup.find_element(By.CSS_SELECTOR, "footer")

    buttons = footer.find_elements(By.CSS_SELECTOR, "button")

    assert len(buttons) == 2

def test_search_bar(driver):
    driver.get("http://localhost:3000")
    time.sleep(3)

    input_element = driver.find_element(By.CSS_SELECTOR,
                                             'input[aria-label="Search by colour, status, shelf, or type..."]')

    # Assert the aria-label matches the expected value
    aria_label_value = input_element.get_attribute('aria-label')
    assert aria_label_value == "Search by colour, status, shelf, or type..."

# TODO: Make test to assess status once material migration is complete