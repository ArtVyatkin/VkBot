import unittest
from crawlers.politeh_crawler import PolitehCrawler


class PolitehCrawlerUnitTests(unittest.TestCase):
    def test_correct_theme(self):
        self.assertEquals(PolitehCrawler.standardize_theme("Достижения"), "Достижения студентов")

    def test_theme_not_in_list(self):
        self.assertEquals(PolitehCrawler.standardize_theme("Достижения "), "Разное")

    def test_theme_is_incorrect(self):
        self.assertEquals(PolitehCrawler.standardize_theme("a"), "Разное")


if __name__ == '__main__':
    unittest.main()
