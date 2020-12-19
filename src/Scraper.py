from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
import random
import time


class Scraper:
    pathToBrowserDriver = "/Users/perez/Desktop/PlayStationDeals/src/chromedriver"

    def __init__(self):
        self.driver = None
        self.list_of_games = []
        self.list_of_non_games = []
        self.next_page_button_enabled = False
        self.rangeToSleep = [0.8, 3.3]

    def start(self):
        self.driver = webdriver.Chrome(self.pathToBrowserDriver)
        self.driver.get("https://store.playstation.com/en-us/category/35027334-375e-423b-b500-0d4d85eff784/1")
        assert "Official PlayStation™Store US" in self.driver.title
        self.driver.implicitly_wait(15)

        while True:
            sleep_time = random.uniform(self.rangeToSleep[0], self.rangeToSleep[1])
            WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR,
                                                  "#main > section > div > div > ul > li:nth-child(1) > div > a > div > div.ems-sdk-product-tile-image__container > span.psw-illustration.psw-illustration--default-product-image.default-product-img"))
            )

            elements = self.driver.find_elements_by_css_selector("#main > section > div > div > ul > li")
            self.next_page_button_enabled = self.is_next_page_enabled()
            for game in elements:
                non_game = False
                split_text = self.splitStringByNewlines(game.text)

                if not self.hasConsole(split_text):
                    print("Missing console", end=": ")
                    print(split_text)
                    non_game = True

                if not self.last_index_is_full_price(split_text) or not self.second_to_last_index_is_full_price(
                        split_text):
                    print("Missing prices", end=": ")
                    print(split_text)
                    continue

                if not self.has_discount(split_text):
                    print("Missing discount", end=": ")
                    print(split_text)
                    continue

                try:
                    title = self.get_game_title(split_text)
                except ValueError as e:
                    print("Unable to get title", end=": ")
                    print(e)
                    continue

                consoles = []
                game_list = []

                try:
                    if self.get_console_index(split_text) == 1:
                        consoles.append(split_text[0])
                        consoles.append(split_text[1])
                    elif self.get_console_index(split_text) == 0:
                        consoles.append(split_text[0])
                except ValueError:
                    pass

                if not non_game:
                    game_list.append(consoles)

                game_list.append(title)
                game_list.append(split_text[-3])
                game_list.append(split_text[-2])
                game_list.append(split_text[-1])

                if not non_game:
                    self.list_of_games.append(game_list)
                else:
                    self.list_of_non_games.append(game_list)

            if not self.next_page_button_enabled:
                break

            print("Sleeping for " + str(sleep_time) + "ms")
            time.sleep(sleep_time)
            self.click_next_page()

        self.driver.close()

    def splitStringByNewlines(self, text):
        return text.splitlines()

    def hasConsole(self, gameText):
        if len(gameText) < 3:
            return False

        if gameText[0] == 'PS4' or gameText[0] == 'PS5':
            return True
        if gameText[1] == 'PS4' or gameText[1] == 'PS5':
            return True
        return False

    def get_console_index(self, game_text):
        if not self.hasConsole(game_text):
            raise ValueError("There are no consoles on this list")

        if game_text[1] == 'PS4' or game_text[1] == 'PS5':
            return 1
        if game_text[0] == 'PS4' or game_text[0] == 'PS5':
            return 0

    def get_game_title(self, game_text):
        try:
            console_index = self.get_console_index(game_text)
            list_fixed_size = len(game_text) - (console_index + 1)

            if list_fixed_size < 3:
                raise ValueError("List does not have enough elements")

            return game_text[console_index + 1]
        except ValueError:
            return game_text[0]

    def last_index_is_full_price(self, game_text):
        x = re.findall("^\$\d*\d\.\d\d$", game_text[-1])

        if len(x) > 0:
            return True
        else:
            return False

    def second_to_last_index_is_full_price(self, game_text):
        x = re.findall("^\$\d*\d\.\d\d$", game_text[-2])

        if len(x) > 0:
            return True
        else:
            return False

    def has_discount(self, game_text):
        x = re.findall("^-\d+%$", game_text[-3])

        if len(x) > 0:
            return True
        else:
            return False

    def is_next_page_enabled(self):
        return self.driver.find_element_by_css_selector(
            "#main > section > div > div > div > div > div > button:nth-child(3)").is_enabled()

    def click_next_page(self):
        self.driver.find_element_by_css_selector(
            "#main > section > div > div > div > div > div > button:nth-child(3)").click()
