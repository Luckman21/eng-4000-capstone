import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

TEST_URL = 'http://127.0.0.1:3000'


def log_admin_in(driver):

    # Go to url and wait until the form shows
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

    username_textbox.send_keys("scream777") #TODO make actual dummy users named "DUMMY USER"

    password = form.find_elements(By.CSS_SELECTOR, "div")[1]
    password_textbox = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Password"]')

    # Verify we got the right input
    aria_label_value = password_textbox.get_attribute('aria-label')
    assert aria_label_value == "Password"

    password_textbox.send_keys("scary4578")#TODO make actual dummy users named "DUMMY USER"

    submit_button = form.find_element(By.CSS_SELECTOR, "button")
    submit_button.click()
    form.submit()
    set_cookie(driver)


def log_super_admin_in(driver):

    # Go to url and wait until the form shows
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

    username_textbox.send_keys("water_123") #TODO make actual dummy users named "DUMMY USER"

    password = form.find_elements(By.CSS_SELECTOR, "div")[1]
    password_textbox = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Password"]')

    # Verify we got the right input
    aria_label_value = password_textbox.get_attribute('aria-label')
    assert aria_label_value == "Password"

    password_textbox.send_keys("Gucci2001")#TODO make actual dummy users named "DUMMY USER"

    submit_button = form.find_element(By.CSS_SELECTOR, "button")
    submit_button.click()
    form.submit()
    set_cookie(driver)

def set_cookie(driver):
    driver.delete_all_cookies()  # Clear existing cookies
    # Set cookie after login
    cookie = {
        'name': 'access_token',
        'value': 'your_token_value_here',
        'domain': '127.0.0.1',
        'path': '/',
    }
    driver.add_cookie(cookie)

    driver.get("http://127.0.0.1:3000/inventory")  # Reload page after setting cookie
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))






