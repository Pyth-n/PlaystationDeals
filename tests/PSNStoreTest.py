import unittest
import time
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class PSNStoreTest(unittest.TestCase):
    pathToBrowserDriver = "/Users/perez/Desktop/PlayStationDeals/src/chromedriver"

    def setUp(self) -> None:
        self.driver = webdriver.Chrome(self.pathToBrowserDriver)
        self.link = "https://store.playstation.com/en-us/category/35027334-375e-423b-b500-0d4d85eff784/1"

    def test_url(self):
        is_valid = re.findall("store\.playstation\.com\/en-us\/category\/([A-z0-9]{8})-([A-z0-9]{4})-([A-z0-9]{4})-([A-z0-9]{4})-([A-z0-9]{12})", self.link)
        self.assertTrue(is_valid)

    def test_a_game_loads(self):
        driver = self.driver
        driver.get(self.link)
        try:
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                  "#main > section > div > div > ul > li:nth-child(1) > div > a > div > div.ems-sdk-product-tile-image__container > span.psw-illustration.psw-illustration--default-product-image.default-product-img"))
            )
        except TimeoutException:
            self.fail("Web drivevr did not find a game!")
        finally:
            time.sleep(3)

    def test_game_properties(self):
        driver = self.driver
        driver.get(self.link)

        try:
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, "#main > section > div > div > ul > li:nth-child(1) > div > a > section")
                )
            )
        except TimeoutException:
            self.fail("Unable to locate game properties")

    

    def tearDown(self) -> None:
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
