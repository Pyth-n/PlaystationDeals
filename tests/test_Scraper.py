from unittest import TestCase
from src.Scraper import Scraper
from selenium import webdriver

class TestScraper(TestCase):
    def setUp(self) -> None:
        self.scraper = Scraper()

    def test_has_console(self):
        text1 = ['PS4', 'Injustice™ 2 - Legendary Edition', '-80%', '$11.99', '$59.99']
        text2 = ['PS5', 'PS4', 'Borderlands 3 Season Pass PS4™ & PS5™', '-40%', '$29.99', '$49.99']
        text3 = ['Borderlands 3 Season Pass PS4™ & PS5™', '-40%', '$29.99', '$49.99']

        self.assertTrue(self.scraper.hasConsole(text1), True)
        self.assertTrue(self.scraper.hasConsole(text2), True)
        self.assertFalse(self.scraper.hasConsole(text3), False)

    def test_get_console_index(self):
        text1 = ['PS4', 'Injustice™ 2 - Legendary Edition', '-80%', '$11.99', '$59.99']
        text2 = ['PS5', 'PS4', 'Borderlands 3 Season Pass PS4™ & PS5™', '-40%', '$29.99', '$49.99']

        self.assertEqual(self.scraper.get_console_index(text1), 0)
        self.assertEqual(self.scraper.get_console_index(text2), 1)

    def test_get_console_index_raises(self):
        text3 = ['Borderlands 3 Season Pass PS4™ & PS5™', '-40%', '$29.99', '$49.99']
        text4 = ['Borderlands 3 Season Pass PS4™ & PS5™', '$49.99']
        with self.assertRaises(ValueError):
            self.scraper.get_console_index(text4)
        with self.assertRaises(ValueError):
            self.scraper.get_console_index(text3)

    def test_get_game_title(self):
        text1 = ['PS4', 'Injustice™ 2 - Legendary Edition', '-80%', '$11.99', '$59.99']
        text2 = ['PS5', 'PS4', 'Borderlands 3 Season Pass PS4™ & PS5™', '-40%', '$29.99', '$49.99']

        self.assertEqual(self.scraper.get_game_title(text1), 'Injustice™ 2 - Legendary Edition')
        self.assertEqual(self.scraper.get_game_title(text2), 'Borderlands 3 Season Pass PS4™ & PS5™')

    def test_last_index_is_full_price(self):
        text1 = ['PS4', 'Injustice™ 2 - Legendary Edition', '-80%', '$11.99', '$9.99']
        text2 = ['PS5', 'PS4', 'Borderlands 3 Season Pass PS4™ & PS5™', '-40%', '$29.99', '$49.99']
        text3 = ['Borderlands 3 Season Pass PS4™ & PS5™', '-40%']

        self.assertEqual(self.scraper.last_index_is_full_price(text1), True)
        self.assertEqual(self.scraper.last_index_is_full_price(text2), True)
        self.assertEqual(self.scraper.last_index_is_full_price(text3), False)

    def test_second_to_last_index_is_full_price(self):
        text1 = ['PS4', 'Injustice™ 2 - Legendary Edition', '-80%', '$11.99', '$59.99']
        text2 = ['PS5', 'PS4', 'Borderlands 3 Season Pass PS4™ & PS5™', '-40%', '$29.99', '$49.99']
        text3 = ['Borderlands 3 Season Pass PS4™ & PS5™', '-40%', '$8.99']

        self.assertEqual(self.scraper.second_to_last_index_is_full_price(text1), True)
        self.assertEqual(self.scraper.second_to_last_index_is_full_price(text2), True)
        self.assertEqual(self.scraper.second_to_last_index_is_full_price(text3), False)

    def test_has_discount(self):
        text1 = ['PS4', 'Injustice™ 2 - Legendary Edition', '-80%', '$11.99', '$59.99']
        text2 = ['PS5', 'PS4', 'Borderlands 3 Season Pass PS4™ & PS5™', '$29.99', '$49.99']
        text3 = ['Borderlands 3 Season Pass PS4™ & PS5™', '-40%', '$8.99']
        text4 = ['PS5', 'PS4', 'Borderlands 3 Season Pass PS4™ & PS5™', '-40%', '$29.99', '$49.99']

        self.assertTrue(self.scraper.has_discount(text1))
        self.assertFalse(self.scraper.has_discount(text2))
        self.assertFalse(self.scraper.has_discount(text3))
        self.assertTrue(self.scraper.has_discount(text4))
