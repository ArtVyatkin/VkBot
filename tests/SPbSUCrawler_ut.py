import unittest
from crawlers.SPbSU_crawler import SPbSUCrawler


class SPbSUCrawlerUnitTests(unittest.TestCase):
    def test_correct_theme(self):
        self.assertEquals(SPbSUCrawler.standardize_theme("achievements"), "Достижения университета")

    def test_theme_not_in_list(self):
        self.assertEquals(SPbSUCrawler.standardize_theme("Достижения "), "Разное")

    def test_theme_is_incorrect(self):
        self.assertEquals(SPbSUCrawler.standardize_theme("a"), "Разное")


if __name__ == '__main__':
    unittest.main()
