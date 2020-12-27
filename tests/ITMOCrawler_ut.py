import unittest
from crawlers.ITMO_crawler import ITMOCrawler


class ITMOCrawlerUnitTests(unittest.TestCase):
    def test_correct_theme(self):
        self.assertEquals(ITMOCrawler.standardize_theme("achievements"), "Достижения университета")

    def test_theme_not_in_list(self):
        self.assertEquals(ITMOCrawler.standardize_theme("Достижения "), "Разное")

    def test_theme_is_incorrect(self):
        self.assertEquals(ITMOCrawler.standardize_theme("a"), "Разное")


if __name__ == '__main__':
    unittest.main()
