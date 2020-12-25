# https://sites.google.com/a/chromium.org/chromedriver/downloads
import re
from src.Scraper import Scraper


def is_url_valid(url_input):
    return re.findall(
        "store\.playstation\.com\/en-us\/category\/([A-z0-9]{8})-([A-z0-9]{4})-([A-z0-9]{4})-([A-z0-9]{4})-([A-z0-9]{"
        "12})",
        url_input)


if __name__ == "__main__":
    is_input_valid = False
    url = None

    print("Format accepted: store.playstation.com/en-us/category/*-*-*-*-*/*\n")

    while not is_input_valid:
        url = input("Enter Playstation deal link: ")

        if is_url_valid(url):
            is_input_valid = True
            print("URL accepted. Preparing to scrape deals...")
        else:
            print("Invalid format, please try again")

    scraper = Scraper(url)
    scraper.start()
