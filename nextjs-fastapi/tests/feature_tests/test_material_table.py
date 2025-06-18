import pytest
import time
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import re
import os
from tests.feature_tests.login_helper import log_admin_in, log_super_admin_in


TEST_URL = "http://127.0.0.1:3000/inventory"

DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)


@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option("prefs", {
         "download.default_directory": DOWNLOAD_DIR,
         "download.prompt_for_download": False,
         "download.directory_upgrade": True,
         "safebrowsing.enabled": True
    })
    chrome_options.add_argument("--window-size=1920,1080")

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

    assert header_text == "ID MATERIAL TYPE COLOUR MASS (g) SHELF STATUS SUPPLIER LINK ACTIONS" or header_text == "ID COLOUR SUPPLIER LINK MASS (g) MATERIAL TYPE SHELF STATUS"


def test_material_table_buttons(driver, login):
    driver.get(TEST_URL)
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
    rows = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr"))
    )

    rows = driver.find_elements(By.CLASS_NAME, "relative flex items-center gap-2")

    # Check each row for the presence of four SVG elements
    for index, row in enumerate(rows):
        WebDriverWait(row, 120).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "svg")))
        svg_elements = row.find_elements(By.TAG_NAME, "svg")

        assert len(svg_elements) == 4, f"Row {index + 1} does not have exactly 4 SVG elements."


def test_material_table_order(driver, login):

    driver.get(TEST_URL)

    rows = WebDriverWait(driver, 40).until(
        lambda d: d.find_elements(By.XPATH, "//tbody/tr") if len(d.find_elements(By.XPATH, "//tbody/tr")) >= 2 else False
    )

    first_td = rows[0].find_element(By.XPATH, "//tbody/tr[1]/td[1]")
    assert first_td.text == '1'

    second_td = rows[1].find_element(By.XPATH, "//tbody/tr[2]/td[1]")
    assert second_td.text == '2'


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
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//tbody/tr[1]/td[3]")))

    first_td = driver.find_element(By.XPATH, "//tbody/tr[1]/td[3]")

    # Levenstien Distance
    assert re.search("Re.", first_td.text) or re.search(".ed", first_td.text) or re.search("R.d", first_td.text) or re.search("..d", first_td.text) or re.search("R..", first_td.text) or re.search(".e.", first_td.text)


def test_status_query(driver, login):
    driver.get(TEST_URL)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search by colour, status, shelf, or type..."]')))

    input_element = driver.find_element(By.CSS_SELECTOR,
                                            'input[aria-label="Search by colour, status, shelf, or type..."]')

    # Status
    input_element.send_keys("In Stock")
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//tbody/tr[1]/td[6]")))

    first_td = driver.find_element(By.XPATH, "//tbody/tr[1]/td[6]")
    assert first_td.text == 'In Stock'


def test_shelf_query(driver, login):
    driver.get(TEST_URL)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search by colour, status, shelf, or type..."]')))

    input_element = driver.find_element(By.CSS_SELECTOR,
                                        'input[aria-label="Search by colour, status, shelf, or type..."]')
    # Shelf
    input_element.send_keys("1")
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//tbody/tr[1]/td[5]")))

    first_td = driver.find_element(By.XPATH, "//tbody/tr[1]/td[5]")
    assert first_td.text == '1'


def test_type_query(driver, login):
    driver.get(TEST_URL)

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Search by colour, status, shelf, or type..."]')))

    input_element = driver.find_element(By.CSS_SELECTOR,
                                        'input[aria-label="Search by colour, status, shelf, or type..."]')
    # Type
    input_element.send_keys("PLA")
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//tbody/tr[1]/td[2]")))

    first_td = driver.find_element(By.XPATH, "//tbody/tr[1]/td[2]")
    # Levenstien Distance
    assert re.search("PL.", first_td.text) or re.search(".LA",first_td.text) or re.search("P.A",first_td.text)


def test_export_materials(driver, login):
    driver.get(TEST_URL)

    time.sleep(3)

    export_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Export CSV')]")
    export_button.click()

    time.sleep(5)

    downloaded_files = os.listdir(DOWNLOAD_DIR)
    matching_files = [f for f in downloaded_files if "materials.csv" in f]
    assert len(matching_files) > 0, "No materials.csv file was downloaded."

    for f in matching_files:
        os.remove(os.path.join(DOWNLOAD_DIR, f))


def test_popovers(driver, login):
    cell_xpaths = [
        "//table//tr[1]/td[2]",
        "//table//tr[1]/td[3]"
    ]
    for xpath in cell_xpaths:

        cell = driver.find_element(By.XPATH, xpath)
        clickable_span = cell.find_element(By.CSS_SELECTOR, "span")
        clickable_span.click()

        # Wait for the popover content to become visible
        wait = WebDriverWait(driver, 10)
        popover = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "whitespace-pre-wrap")))

        assert popover.is_displayed(), "Popover did not appear after clicking the cell."
        assert popover.text.strip() != "", "Popover content is empty."
