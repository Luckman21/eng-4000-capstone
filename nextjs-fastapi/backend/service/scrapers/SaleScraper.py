import sys
from pathlib import Path
import json
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from db.repositories.MaterialRepository import MaterialRepository
from db.repositories.MaterialTypeRepository import MaterialTypeRepository
from db.repositories.UserRepository import UserRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.controller import constants
from backend.service.mailer.SaleMailer import SaleMailer
import time
from selenium.webdriver import Remote
import chromedriver_autoinstaller
import re


def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # This means you won't see the actual icon
    chrome_options.add_argument("--disable-gpu") # Disable GPU acceleration (required in headless mode)
    chrome_options.add_argument("--no-sandbox")  # Might help in some environments
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/58.0.3029.110 Safari/537.36")
    chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent crashes in Docker
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection
    chrome_options.add_argument("--window-size=1920x1080")  # Ensure full page is loaded

    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def setup_database():
    engine = create_engine(constants.DATABASE_URL_TEST, echo=True)

    # Create a session factory bound to the engine
    Session = sessionmaker(bind=engine)
    session = Session()

    return session

def scrape_amazon_page_for_sale(url, driver):
    driver.get(url)
    time.sleep(10)

    # Let's see if the sale exists. If not return false
    name = 'a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin ' \
               'savingsPercentage '
    sale = driver.find_elements(By.CLASS_NAME, name)

    name = 'offersConsistencyEnabled'
    coupon = driver.find_elements(By.CLASS_NAME, name)

    if coupon is None and sale is None:
        return False, ''
    elif sale:
        return True, ''

    return True, ''


def scrape_digitkey_page_for_sale(url, driver) -> bool:
    driver.get(url)
    session = setup_database()

    # Let's see if the sale exists. If not return false
    try:
        original_price = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "comparePrice")))
        current_price = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "productPrice")))
    except TimeoutException:
        return False, None

    current_price_float = float(current_price.text.replace("$", ""))
    original_price_float = float(original_price.text.replace("$", ""))
    pct_off = (current_price_float / original_price_float) * 100.00


    return True, str(round(pct_off, 2))


def run():

    # Set up
    driver = init_driver()
    session = setup_database()
    material_repo = MaterialRepository(session)
    material_type_repo = MaterialTypeRepository(session)
    user_repo = UserRepository(session)

    # Get materials
    materials = material_repo.get_all_materials()
    items_on_sale = []

    # Look for a sale in each material
    for material in materials:
        link = material.supplier_link

        # Find proper website using regex
        pattern = re.compile(r"amazon", re.IGNORECASE)
        amazon_match = pattern.search(link)

        pattern = re.compile(r"digitmakers", re.IGNORECASE)
        digitmakers_match = pattern.search(link)

        sale_found = False

        # Find regex match
        if amazon_match:
           sale_found, text = scrape_amazon_page_for_sale(link, driver)

        elif digitmakers_match:
            sale_found, text = scrape_digitkey_page_for_sale(link, driver)

        # If a sale is found, let's add their colour and material type name to the list
        if sale_found:
            mattype = material_type_repo.get_material_type_by_id(material.material_type_id)
            items_on_sale.append(f'<li>{material.colour} {mattype.type_name} {text}: <a href="{material.supplier_link}">View Details</a></li>')


    # If sales were found, send an email
    if len(items_on_sale) > 0:

        result_as_newline_separated_string = "<ul>" + "\n".join(items_on_sale) + "</ul>"

        mailer = SaleMailer(from_addr=constants.MAILER_EMAIL)
        super_admins = user_repo.get_all_superadmins()

        for super_admin in super_admins:
            mailer.send_notification(super_admin.email, result_as_newline_separated_string)

    output_file = "scraper_output.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(items_on_sale, f, indent=4)

if __name__ == "__main__":
    run()
