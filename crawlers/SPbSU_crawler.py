from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from config import months_dict
from .crawler import Crawler


class SPbSUCrawler(Crawler):
    def __init__(self, start_date, keywords):
        self.start_date = start_date
        self.keywords = keywords
        self.browser = webdriver.Chrome('/home/artvyatkin/chromedriver')
        self.data = pd.DataFrame(columns=["university", "title", "link", "date", "photo_link"])

    def parse_page_in_table(self, number_of_page):
        self.browser.get("https://spbu.ru/news-events/novosti" + number_of_page)
        page_root = BeautifulSoup(self.browser.page_source, "lxml")
        table = page_root.find(
            "div",
            {
                "class": "col-xs-12 col-md-9 col-lg-8 card-list--medium card-list--context card-list-clear-sm card-context--clear"
            }
        )  # to locate it definitely
        for news_card in table.find_all("div", class_="card-context--large"):
            try:
                string_date = news_card.find("span", {"class": "card__date"}).text.lower()
                for russian, english in months_dict.items():
                    string_date = string_date.replace(russian, english)
                date = datetime.strptime(string_date, "%d %b %Y")
                if date > self.start_date:
                    title = news_card.find("h4", {"class": "card__title"}).text
                    # for keyword in self.keywords:
                    #     if keyword in title:
                    # photo_link = news_card.find("div", {"class": "card__img"}).get("style")[23:-2]
                    link = "https://www.spbu.ru" + news_card.find("a", {"class": "card__header"}).get("href")

                    self.browser.get(link)
                    page_root_2 = BeautifulSoup(self.browser.page_source, "lxml")
                    poster = page_root_2.find("div", {"class": "event-poster"})
                    if poster is None:
                        photo_link = news_card.find("div", {"class": "card__img"}).get("style")[23:-2]
                    else:
                        photo_link = poster.find("img").get("src")
                    self.data.loc[0 if pd.isnull(self.data.index.max()) else self.data.index.max() + 1] = \
                        ["SPbSU", title, link, string_date, photo_link]  # append
            except BaseException:
                print("!")

    def get_news(self):
        self.parse_page_in_table("")
        for number in range(1, 6):
            self.parse_page_in_table("?page=" + str(number))

        self.data.drop_duplicates(inplace=True)
        self.data = self.data.reset_index(
            drop=True)  # otherwise some indexes after deleting of duplicates will be missing
        # drop=True shows that it doesn't need to remain old indexes in index column
        # self.data.to_excel("SPbSU.xlsx")
        self.browser.quit()
        return self.data
