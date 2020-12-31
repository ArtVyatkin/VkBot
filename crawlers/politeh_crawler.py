from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from config import months_dict
from .crawler import Crawler


class PolitehCrawler(Crawler):
    def __init__(self, start_date, keywords):
        self.start_date = start_date
        self.keywords = keywords
        self.browser = webdriver.Chrome('/home/artvyatkin/chromedriver')
        self.data = pd.DataFrame(columns=["university", "title", "link", "date", "photo_link", "theme"])
        self.sections = ["Достижения", "Наука и инновации", "Культура", "Международная деятельность", "Образование",
                         "Партнёрство", "Политех МЕДИА", "Спорт", "Университетская жизнь"]

    @staticmethod
    def standardize_theme(theme):
        themes_dict = {
            "Достижения": "Достижения студентов",
            "Наука и инновации": "Наука",
            "Культура": "Жизнь университета",
            "Международная деятельность": "Сотрудничество и партнёрство",
            "Партнёрство": "Сотрудничество и партнёрство",
            "Политех МЕДИА": "Разное",
            "Спорт": "Жизнь университета",
            "Университетская жизнь": "Жизнь университета"
        }
        if theme in themes_dict:
            theme = themes_dict[theme]
        else:
            theme = "Разное"
        return theme

    def parse_page_in_table(self, chapter):
        self.browser.get("https://spbstu.ru/")
        self.browser.find_element_by_link_text("все новости").click()
        self.browser.find_element_by_link_text(chapter).click()
        page_root = BeautifulSoup(self.browser.page_source, "lxml")
        table = page_root.find("div", {"class": "news-list clearfix"})
        for news_card in table.findChildren("div", recursive=False):
            string_date = news_card.find("div", class_="article-date").text.split(",")[1].lower()
            for russian, english in months_dict.items():
                string_date = string_date.replace(russian, english)
            date = datetime.strptime(string_date, " %d %b %Y")
            if date > self.start_date:
                block = news_card.find("h4")
                title = block.text
                photo_link = "https://www.spbstu.ru" + news_card.find("img", {"class": "img-responsive"}).get("src")
                theme = news_card.find("span", {"class": "article-tag-label"})
                if theme is None:
                    theme = ""
                else:
                    theme = theme.text
                theme = self.standardize_theme(theme)

                link = block.find("a").get("href")
                if link[0] != 'h':
                    link = "https://www.spbstu.ru" + link
                self.data.loc[0 if pd.isnull(self.data.index.max()) else self.data.index.max() + 1] = \
                    ["SPbSTU", title, link, date.strftime("%d %b %Y"), photo_link, theme]  # append

    def get_news(self):
        for section in self.sections:
            for number in range(1, 2):
                self.parse_page_in_table(section)

        self.data.drop_duplicates(inplace=True)
        self.data = self.data.reset_index(drop=True)
        self.browser.quit()
        return self.data
