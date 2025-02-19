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



TEST_URL = "http://127.0.0.1:3000/inventory"

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
    log_super_admin_in(driver)
    time.sleep(3)


def test_material_table_header(driver, login):
    driver.get(TEST_URL)
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
    rows = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr"))
    )

    # Find the header row
    header_row = driver.find_element(By.CSS_SELECTOR, "thead tr")

    # Get the full text of the header row (all titles in one string)
    header_text = header_row.text

    assert header_text == "ID COLOUR SUPPLIER LINK MASS (g) MATERIAL TYPE SHELF STATUS ACTIONS" or header_text == "ID COLOUR SUPPLIER LINK MASS (g) MATERIAL TYPE SHELF STATUS"


def test_material_table_buttons(driver, login):
    driver.get(TEST_URL)
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
    rows = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr"))
    )

    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

    # Check each row for the presence of two SVG elements
    for index, row in enumerate(rows):
        WebDriverWait(row, 60).until(EC.visibility_of_element_located((By.TAG_NAME, "svg")))
        svg_elements = row.find_elements(By.TAG_NAME, "svg")

        # Assert that each row has exactly 2 SVGs (or adjust as necessary)
        assert len(svg_elements) == 4, f"Row {index + 1} does not have exactly 4 SVG elements."

def test_material_table_order(driver, login):

    driver.get(TEST_URL)
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
    rows = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr"))
    )

    for _ in range(3):
        try:
            first_td = driver.find_element(By.XPATH, "//tbody/tr[1]/td[1]")
            assert first_td.text == '1'

            second_td = driver.find_element(By.XPATH, "//tbody/tr[2]/td[1]")
            assert second_td.text == '2'
            break
        except StaleElementReferenceException:
            time.sleep(1)


def test_edit_button(driver, login):

    driver.get(TEST_URL)
    WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.XPATH, "//tbody/tr[1]/td[8]")))

    button = driver.find_element(By.XPATH, "//tbody/tr[1]/td[8]/div/span[2]")
    button.click()

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, "section")))

    panel = driver.find_element(By.TAG_NAME, "section")

    header = panel.find_element(By.CSS_SELECTOR, "header")

    assert header.text == "Edit Material"

    labels = panel.find_elements(By.CSS_SELECTOR, "label")

    assert labels[0].text == "Supplier Link"
    assert labels[1].text == "Colour"
    assert labels[2].text == "Weight (g)"
    assert labels[3].text == "Shelf"
    assert labels[4].text == "Material Type"

def test_replenish_button(driver, login):

    driver.get(TEST_URL)
    WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.XPATH, "//tbody/tr[1]/td[8]")))

    button = driver.find_element(By.XPATH, "//tbody/tr[1]/td[8]/div/span[1]")
    button.click()

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, "section")))

    panel = driver.find_element(By.TAG_NAME, "section")

    header = panel.find_element(By.CSS_SELECTOR, "header")

    assert header.text == "Add/Remove Material"

    labels = panel.find_elements(By.CSS_SELECTOR, "label")

    assert labels[0].text == "Colour"
    assert labels[1].text == "Material Type"
    assert labels[2].text == "Weight (g)"

    # Get buttons (slider stuff at the top)

    buttons = panel.find_elements(By.CSS_SELECTOR, "button")

    add = buttons[2].find_element(By.CSS_SELECTOR, 'div')
    assert add.text == "Add Mass"

    remove = buttons[3].find_element(By.CSS_SELECTOR, 'div')
    assert remove.text == "Remove Mass"



def test_create_button(driver, login):
    driver.get(TEST_URL)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button")))

    buttons = driver.find_elements(By.CSS_SELECTOR, "button")
    button = buttons[0]
    button.click()
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, "section")))

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


def test_delete_confirmation(driver, login):
    driver.get(TEST_URL)
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
    rows = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr"))
    )

    for _ in range(3):
        try:
            row = rows[0]
            print(row.text)

            driver.get(TEST_URL)
            WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.XPATH, "//tbody/tr[1]/td[8]")))

            delete_icon = driver.find_element(By.XPATH, "//tbody/tr[1]/td[8]/div/span[3]")
            delete_icon.click()

            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, "section")))

            popup = driver.find_element(By.TAG_NAME, "section")

            header = popup.find_element(By.TAG_NAME, "header")
            assert header.text == "Delete Item"

            text = popup.find_element(By.XPATH, "div[2]")
            assert text.text == 'Are you sure you want to delete this item? This action cannot be undone.'

            footer = popup.find_element(By.CSS_SELECTOR, "footer")

            buttons = footer.find_elements(By.CSS_SELECTOR, "button")

            assert len(buttons) == 2
            break
        except StaleElementReferenceException:
            time.sleep(1)


def test_search_bar(driver, login):
    driver.get(TEST_URL)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search by colour, status, shelf, or type..."]')))

    input_element = driver.find_element(By.CSS_SELECTOR,
                                             'input[aria-label="Search by colour, status, shelf, or type..."]')

    # Assert the aria-label matches the expected value
    aria_label_value = input_element.get_attribute('aria-label')
    assert aria_label_value == "Search by colour, status, shelf, or type..."

def test_colour_query(driver, login):
    driver.get(TEST_URL)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search by colour, status, shelf, or type..."]')))

    input_element = driver.find_element(By.CSS_SELECTOR,
                                        'input[aria-label="Search by colour, status, shelf, or type..."]')


    # Colour
    input_element.send_keys("Red")
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//tbody/tr[1]/td[2]")))

    first_td = driver.find_element(By.XPATH, "//tbody/tr[1]/td[2]")

    # Levenstien Distance
    assert re.search("Re.", first_td.text) or re.search(".ed", first_td.text) or re.search("R.d", first_td.text) or re.search("..d", first_td.text) or re.search("R..", first_td.text) or re.search(".e.", first_td.text)

def test_status_query(driver, login):
    driver.get(TEST_URL)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search by colour, status, shelf, or type..."]')))

    input_element = driver.find_element(By.CSS_SELECTOR,
                                            'input[aria-label="Search by colour, status, shelf, or type..."]')

    # Status
    input_element.send_keys("In Stock")
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//tbody/tr[1]/td[7]")))

    first_td = driver.find_element(By.XPATH, "//tbody/tr[1]/td[7]")
    assert first_td.text == 'In Stock'

def test_shelf_query(driver, login):
    driver.get(TEST_URL)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search by colour, status, shelf, or type..."]')))

    input_element = driver.find_element(By.CSS_SELECTOR,
                                        'input[aria-label="Search by colour, status, shelf, or type..."]')
    # Shelf
    input_element.send_keys("1")
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//tbody/tr[1]/td[6]")))

    first_td = driver.find_element(By.XPATH, "//tbody/tr[1]/td[6]")
    assert first_td.text == '1'


def test_type_query(driver, login):
    driver.get(TEST_URL)

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search by colour, status, shelf, or type..."]')))

    input_element = driver.find_element(By.CSS_SELECTOR,
                                        'input[aria-label="Search by colour, status, shelf, or type..."]')
    # Type
    input_element.send_keys("PLA")
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//tbody/tr[1]/td[5]")))

    first_td = driver.find_element(By.XPATH, "//tbody/tr[1]/td[5]")
    # Levenstien Distance
    assert re.search("PL.", first_td.text) or re.search(".LA",first_td.text) or re.search("P.A",first_td.text)

# TODO: Make test to assess status once material migration is complete