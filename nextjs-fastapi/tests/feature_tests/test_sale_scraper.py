import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from backend.service.scrapers.SaleScraper import scrape_amazon_page_for_sale, scrape_digitkey_page_for_sale, run

@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # This means you won't see the actual icon
    chrome_options.add_argument("--disable-gpu") # Disable GPU acceleration (required in headless mode)
    chrome_options.add_argument("--no-sandbox")  # Might help in some environments
    # This will change depending on your driver

    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()  # Cleanup after test

def test_scrape_amazon_page_for_sale_found(driver):
    # Test against a real URL (make sure the page you're testing on has a sale)
    url = 'https://www.amazon.ca/ELEGOO-Filament-Dimensional-Accuracy-Compatible/dp/B0BM95MYNX/ref=sxin_15_pa_sp_search_thematic_sspa?content-id=amzn1.sym.46621be6-fabe-4126-8501-d32c96c42a24%3Aamzn1.sym.46621be6-fabe-4126-8501-d32c96c42a24&cv_ct_cx=PLA&keywords=PLA&pd_rd_i=B0BM95MYNX&pd_rd_r=801386cf-36e0-470c-aa3d-fd4084381423&pd_rd_w=usjfA&pd_rd_wg=A4vii&pf_rd_p=46621be6-fabe-4126-8501-d32c96c42a24&pf_rd_r=TQBGZJC1XMJR5CW8WMAX&qid=1739823127&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sr=1-1-acb80629-ce74-4cc5-9423-11e8801573fb-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9zZWFyY2hfdGhlbWF0aWM&th=1'  # Replace with an actual Amazon product URL with a sale
    assert scrape_amazon_page_for_sale(url, driver) is True

def test_scrape_digitmaker_page_for_sale_found(driver):
    # Test against a real URL (make sure the page you're testing on has a sale)
    url = 'https://www.digitmakers.ca/collections/esun-filaments/products/esun-emarble-pla-filament-1-75mm-1kg'  # Replace with an actual Amazon product URL with a sale
    assert scrape_digitkey_page_for_sale(url, driver) is True
