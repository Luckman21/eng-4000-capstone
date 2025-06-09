import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from backend.service.scrapers.SaleScraper import scrape_amazon_page_for_sale, scrape_digitkey_page_for_sale, run

@pytest.fixture
def driver():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/58.0.3029.110 Safari/537.36")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-size=1920x1080")

    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()


def test_scrape_amazon_page_for_sale_found(driver):
    url = 'https://www.amazon.ca/ELEGOO-Filament-Dimensional-Accuracy-Compatible/dp/B0BM95MYNX/ref=sxin_15_pa_sp_search_thematic_sspa?content-id=amzn1.sym.46621be6-fabe-4126-8501-d32c96c42a24%3Aamzn1.sym.46621be6-fabe-4126-8501-d32c96c42a24&cv_ct_cx=PLA&keywords=PLA&pd_rd_i=B0BM95MYNX&pd_rd_r=801386cf-36e0-470c-aa3d-fd4084381423&pd_rd_w=usjfA&pd_rd_wg=A4vii&pf_rd_p=46621be6-fabe-4126-8501-d32c96c42a24&pf_rd_r=TQBGZJC1XMJR5CW8WMAX&qid=1739823127&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sr=1-1-acb80629-ce74-4cc5-9423-11e8801573fb-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9zZWFyY2hfdGhlbWF0aWM&th=1'
    bool = scrape_amazon_page_for_sale(url, driver)
    assert bool is True

#TODO digikey website is broken. If Pantheon intends on reinstating this feature and digikey's website is fine, restore this test

# def test_scrape_digitmaker_page_for_sale_found_1(driver):
#     url = 'https://www.digitmakers.ca/collections/esun-filaments/products/esun-emarble-pla-filament-1-75mm-1kg'
#     bool = scrape_digitkey_page_for_sale(url, driver)
#     assert bool is True
#
#
# def test_scrape_digitmaker_page_for_sale_found_2(driver):
#     url = 'https://www.digitmakers.ca/collections/offer-of-the-week-3d-printing-canada-3d-filaments-canada/products/d3d-premium-petg-filament-1-75-mm-1kg-spool?variant=8112650649636'
#     bool = scrape_digitkey_page_for_sale(url, driver)
#     assert bool is True
