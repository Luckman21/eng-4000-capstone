import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from tests.feature_tests.login_helper import log_admin_in, log_super_admin_in

TEST_URL = "http://127.0.0.1:3000/userProfile"


@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=chrome_options)

    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def login(driver):
    log_super_admin_in(driver)
    time.sleep(3)


# NOTE: Since the page is relatively static, I'm testing in one go to minimize wait time
def test_user_profile(driver, login):
    driver.get(TEST_URL)
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))

    # Test header
    header = driver.find_element(By.CSS_SELECTOR, "h1")
    assert header.text == 'User Profile'

    # Test labels
    labels = driver.find_elements(By.CSS_SELECTOR, 'label')

    assert labels[0].text == 'Username'
    assert labels[1].text == 'Email'

    # Test Inputs

    textboxes = driver.find_elements(By.CSS_SELECTOR, "input")
    assert textboxes[0].get_attribute('placeholder') == 'Enter username'
    assert textboxes[1].get_attribute('placeholder') == 'Enter user email'

    # Test buttons

    buttons = driver.find_elements(By.CSS_SELECTOR, "button")

    update = buttons[0]
    save = buttons[1]

    assert update.text == 'Update Password'
    assert save.text == 'Save Changes'

def test_password_update(driver, login):
    driver.get(TEST_URL)
    WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))

    buttons = driver.find_elements(By.CSS_SELECTOR, "button")
    update = buttons[0]
    update.click()

    section = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR, "section")))

    header = section.find_element(By.CSS_SELECTOR, "header")
    assert header.text == 'Edit Password'

    labels = section.find_elements(By.CSS_SELECTOR, "label")
    assert labels[0].text == 'New Password'
    assert labels[1].text == 'Confirm Password'

    inputs = section.find_elements(By.CSS_SELECTOR, 'input')

    inputs[0].send_keys('random password')
    inputs[1].send_keys('doesn\'t match')

    footer = section.find_element(By.CSS_SELECTOR, 'footer')
    buttons = footer.find_elements(By.CSS_SELECTOR, 'button')
    buttons[1].click()

    WebDriverWait(section, 10).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "text-danger"),  "Passwords do not match")
    )


