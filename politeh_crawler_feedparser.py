import feedparser
import pandas as pd
from crawlers.politeh_crawler import PolitehCrawler
import dateutil.parser as dparser


class PolitehCrawlerFeedparser:
    def __init__(self, start_date, keywords):
        self.start_date = start_date
        self.keywords = keywords
        self.data = pd.DataFrame(columns=["university", "title", "link", "date", "photo_link", "theme"])
        self.sections = ["Достижения", "Наука и инновации", "Культура", "Международная деятельность", "Образование",
                         "Партнёрство", "Политех МЕДИА", "Спорт", "Университетская жизнь"]

    def get_news(self, entries=None):
        if entries is None:
            entries = feedparser.parse("https://www.spbstu.ru/media/news/rss/")["entries"]

        for entry in entries:
            title = entry["title"]
            link = entry["link"]
            date_original = entry["published"]
            date = dparser.parse(date_original, fuzzy=True)
            string_date = date.strftime("%d-%b-%Y")
            photo_link = ""
            for link_to_resource in entry["links"]:
                if "image" in link_to_resource["type"]:
                    photo_link = link_to_resource["href"]
                    break
            theme = PolitehCrawler.standardize_theme(entry["tags"][0]["term"].replace("/", "").strip())

            self.data.loc[0 if pd.isnull(self.data.index.max()) else self.data.index.max() + 1] = \
                ["SPbSTU", title, link, string_date, photo_link, theme]  # append
        with pd.option_context('display.max_rows', None, 'display.max_columns', None, "display.max_colwidth", 10000):
            print(self.data)
        self.data.drop_duplicates(inplace=True)
        self.data = self.data.reset_index(drop=True)
        return self.data
