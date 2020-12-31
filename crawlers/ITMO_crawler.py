from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from config import months_dict
from .crawler import Crawler


class ITMOCrawler(Crawler):
    def __init__(self, start_date, keywords):
        self.start_date = start_date
        self.keywords = keywords
        self.browser = webdriver.Chrome('/home/artvyatkin/chromedriver')
        self.data = pd.DataFrame(columns=["university", "title", "link", "date", "photo_link", "theme"])
        self.sections = ["ratings", "achievements", "leisure", "ads", "social_activity"]

    @staticmethod
    def standardize_theme(theme):
        themes_dict = {
            "achievements": "Достижения университета",
            "startup": "Достижения студентов",
            "initiative": "Жизнь университета",
            "partnership": "Сотрудничество и партнёрство",
            "innovations": "Разное",
            "ministry_of_education": "Официальные документы",
            "official": "Официальные документы"
        }
        if theme in themes_dict:
            theme = themes_dict[theme]
        else:
            theme = "Разное"
        return theme

    def parse_page_in_table(self, number_of_page, chapter):
        self.browser.get("https://news.itmo.ru/ru/university_live/" + chapter + "/" + number_of_page)
        page_root = BeautifulSoup(self.browser.page_source, "lxml")
        table = page_root.find("ul", {"class": "triplet"})
        for news_card in table.findChildren("li", recursive=False):
            string_date = news_card.find("time").text.lower()
            for russian, english in months_dict.items():
                string_date = string_date.replace(russian, english)
            date = datetime.strptime(string_date, "%d %b %Y")
            theme = self.standardize_theme(chapter)

            if date > self.start_date:
                block = news_card.find("h4")
                title = block.text
                link = 'https://news.itmo.ru' + block.find("a").get("href")
                photo_link = "https://news.itmo.ru/" + news_card.find("img").get("src")
                self.data.loc[0 if pd.isnull(self.data.index.max()) else self.data.index.max() + 1] = \
                    ["ITMO", title, link, string_date, photo_link, theme]  # append

    def get_news(self):
        for section in self.sections:
            for number in range(1, 3):
                self.parse_page_in_table(str(number), section)

        self.data.drop_duplicates(inplace=True)
        self.data = self.data.reset_index(drop=True)  # otherwise some indexes after deleting of duplicates will be missing
        # drop=True shows that it doesn't need to remain old indexes in index column
        # print(self.data["title"])
        # self.data.to_excel("ITMO.xlsx")
        self.browser.quit()
        return self.data
