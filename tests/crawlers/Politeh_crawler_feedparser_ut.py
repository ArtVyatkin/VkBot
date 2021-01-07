import unittest
import pandas as pd
import json
from politeh_crawler_feedparser import PolitehCrawlerFeedparser


class PolitehCrawlerFeedparserUnitTests(unittest.TestCase):
    def test_empty_rss_channel(self):
        crawler = PolitehCrawlerFeedparser(None, None)
        data = crawler.get_news([])
        self.assert_(pd.DataFrame(columns=["university", "title", "link", "date", "photo_link", "theme"]).equals(data))

    def test_one_record(self):
        crawler = PolitehCrawlerFeedparser(None, None)
        with open("../resources/crawlers/one_record.json", "r", encoding="utf-8") as input_file:
            records = json.loads(input_file.read())
        data = crawler.get_news(records)
        title = "Александра ФИЛАРЕТОВА: «Ничего не бояться, идти к цели, гореть любимым делом и просто раствориться в работе»"
        link = "https://www.spbstu.ru/media/news/politech-media/media-spbstu-207/"
        string_date = "26-Dec-2020"
        photo_link = "https://www.spbstu.ru/upload/iblock/79f/266.jpg"
        theme = "Разное"

        expected_dataframe = pd.DataFrame(columns=["university", "title", "link", "date", "photo_link", "theme"])
        expected_dataframe.loc[0] = ["SPbSTU", title, link, string_date, photo_link, theme]
        self.assert_(expected_dataframe.equals(data))

    def test_several_records(self):
        crawler = PolitehCrawlerFeedparser(None, None)
        with open("../resources/crawlers/one_record.json", "r", encoding="utf-8") as input_file:
            records = json.loads(input_file.read())
        data = crawler.get_news(records)
        title = "Александра ФИЛАРЕТОВА: «Ничего не бояться, идти к цели, гореть любимым делом и просто раствориться в работе»"
        link = "https://www.spbstu.ru/media/news/politech-media/media-spbstu-207/"
        string_date = "26-Dec-2020"
        photo_link = "https://www.spbstu.ru/upload/iblock/79f/266.jpg"
        theme = "Разное"

        expected_dataframe = pd.DataFrame(columns=["university", "title", "link", "date", "photo_link", "theme"])
        expected_dataframe.loc[0] = ["SPbSTU", title, link, string_date, photo_link, theme]
        # expected_dataframe.loc[1] = ["SPbSTU", title, link, string_date, photo_link, theme]

        with pd.option_context('display.max_rows', None, 'display.max_columns', None, "display.max_colwidth", 10000):
            print(expected_dataframe)
        self.assert_(expected_dataframe.equals(data))


if __name__ == '__main__':
    unittest.main()
