import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

TEST_URL = "http://127.0.0.1:3000/QR/1"


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


def test_material_description(driver):
    driver.get(TEST_URL)
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2")))

    # Test header
    title = driver.find_element(By.CSS_SELECTOR, "h2")
    assert title.text == 'TPU - Black'

    subtitles = driver.find_elements(By.CSS_SELECTOR, "p")

    assert subtitles[0].text == "Shelf: 1"
    assert subtitles[1].text == "Enter mass change (grams):"


def test_buttons(driver):
    driver.get(TEST_URL)
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button")))

    # Test header
    buttons = driver.find_elements(By.CSS_SELECTOR, "button")
    assert buttons[0].text == 'Add Mass'
    assert buttons[1].text == 'Remove Mass'
    assert buttons[2].text == 'Cancel'
