import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

TEST_URL = "http://127.0.0.1:3000/"

# LOGIN HELPER ALREADY TESTS SUCCESSFUL LOG IN


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


def test_banner(driver):

    driver.get(TEST_URL)
    image = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "img")))
    assert image is not None


def test_password_failure(driver):
    driver.get(TEST_URL)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "form")))
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Username"]')))
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Password"]')))
    time.sleep(3)

    form = driver.find_element(By.CSS_SELECTOR, "form")

    username = form.find_elements(By.CSS_SELECTOR, "div")[0]
    username_textbox = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Username"]')

    # Verify we got the right input
    aria_label_value = username_textbox.get_attribute('aria-label')
    assert aria_label_value == "Username"

    username_textbox.send_keys("scream777")  # Use actual

    password = form.find_elements(By.CSS_SELECTOR, "div")[1]
    password_textbox = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Password"]')

    # Verify we got the right input
    aria_label_value = password_textbox.get_attribute('aria-label')
    assert aria_label_value == "Password"

    password_textbox.send_keys("password_fake")  # fake

    submit_button = form.find_element(By.CSS_SELECTOR, "button")
    submit_button.click()
    form.submit()

    error = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'p')))
    assert error.text == "Invalid username or password"


def test_username_failure(driver):
    driver.get(TEST_URL)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "form")))
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Username"]')))
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[aria-label="Password"]')))
    time.sleep(3)

    form = driver.find_element(By.CSS_SELECTOR, "form")

    username = form.find_elements(By.CSS_SELECTOR, "div")[0]
    username_textbox = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Username"]')

    # Verify we got the right input
    aria_label_value = username_textbox.get_attribute('aria-label')
    assert aria_label_value == "Username"

    username_textbox.send_keys("fakest_of_fake_usernames")  # Use actual

    password = form.find_elements(By.CSS_SELECTOR, "div")[1]
    password_textbox = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Password"]')

    # Verify we got the right input
    aria_label_value = password_textbox.get_attribute('aria-label')
    assert aria_label_value == "Password"

    password_textbox.send_keys("password_fake")  # fake

    submit_button = form.find_element(By.CSS_SELECTOR, "button")
    submit_button.click()
    form.submit()

    error = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'p')))
    assert error.text == "Invalid username or password"


def test_buttons(driver):
    driver.get(TEST_URL)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "form")))
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div")))
    time.sleep(3)

    form = driver.find_element(By.CSS_SELECTOR, "form")

    submit = form.find_elements(By.CSS_SELECTOR, "button")[0]
    forgot = form.find_elements(By.CSS_SELECTOR, "button")[1]

    assert submit.text == "Login"
    assert forgot.text == "Forgot Password"

    # Test the popup

    forgot.click()
    forgot_password_panel = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "section")))

    # Header
    header = forgot_password_panel.find_element(By.CSS_SELECTOR, "header")
    assert header.text == 'Forgot Password'

    # Textbox
    text = forgot_password_panel.find_element(By.CSS_SELECTOR, "p")
    assert text.text == 'Enter your email to receive a temporary password:'

    textbox_label = forgot_password_panel.find_element(By.CSS_SELECTOR, "label")
    assert textbox_label.text == 'Email'

    textbox = forgot_password_panel.find_element(By.CSS_SELECTOR, "input")
    assert textbox.get_attribute('placeholder') == 'Enter your email'

    # Buttons
    footer = forgot_password_panel.find_element(By.CSS_SELECTOR, "footer")
    buttons = footer.find_elements(By.CSS_SELECTOR, "button")

    cancel = buttons[0]
    submit = buttons[1]

    assert cancel.text == 'Cancel'
    assert submit.text == 'Submit'









