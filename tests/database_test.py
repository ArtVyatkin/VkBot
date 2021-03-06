import json
from datetime import datetime

from database import Database

import unittest


def prepare_database(database, news):
    for i in range(0, 5):
        database.add_user(i, 0)
    for current_news in news:
        database.add_news(current_news["date"], current_news["university"], current_news["title"], current_news["link"],
                          current_news["theme"], current_news["photo_id"])


def clear_unnecessary_data(database, news):
    database.delete_users([i for i in range(0, 5)])
    database.delete_news(map(lambda current_news: current_news["title"], news))


class DatabaseTests(unittest.TestCase):
    db = None
    adding_news = None

    @classmethod
    def setUpClass(cls):
        db = Database()
        with open("tests/resources/database/news_for_adding.json", "r", encoding="utf-8") as input_file:
            adding_news = json.loads(input_file.read())
        prepare_database(db, adding_news)
        cls.db = db
        cls.adding_news = adding_news

    @classmethod
    def tearDownClass(cls):
        clear_unnecessary_data(cls.db, cls.adding_news)

    def test_existing_user(self):
        self.assertTrue(self.db.is_user_exist(2))

    def test_non_existing_user(self):
        self.assertFalse(self.db.is_user_exist(-1))

    def test_get_user(self):
        self.assertEqual(self.db.get_user(3).state, 0)

    def test_set_topics(self):
        self.db.set_topics(1, ["Политех", "ИТМО"])
        self.assertEqual(self.db.get_user(1).topics, ["Политех", "ИТМО"])

    def test_set_topics_empty_topics_list(self):
        self.db.set_topics(2, [])
        self.assertEqual(self.db.get_user(2).topics, [])

    def test_set_universities(self):
        self.db.set_universities(2, ["СПбГУ"])
        self.assertEqual(self.db.get_user(2).universities, ["СПбГУ"])

    def test_set_universities_empty_universities_list(self):
        self.db.set_universities(1, [])
        self.assertEqual(self.db.get_user(1).universities, [])

    def test_set_sending_time(self):
        self.db.set_sending_time(0, 'W-6-13')
        self.assertEqual(self.db.get_user(0).sending_time, 'W-6-13')

    def test_set_user_state(self):
        self.db.set_user_state(0, 10)
        self.assertEqual(self.db.get_user(0).state, 10)

    def test_set_user_state_with_state_payload(self):
        self.db.set_user_state(2, 11, "some_state_payload")
        self.assertEqual(self.db.get_user(2).state_payload, "some_state_payload")

    def test_get_news_by_one_university_check_first_university(self):
        received_news = self.db.get_news(["СПбГУ"])
        self.assertIn("title1", map(lambda current_news: current_news.title, received_news))

    def test_get_news_by_one_university_check_second_university(self):
        received_news = self.db.get_news(["СПбГУ"])
        self.assertIn("title2", map(lambda current_news: current_news.title, received_news))

    def test_get_news_by_one_university_and_last_date_suitable_news(self):
        received_news = self.db.get_news(["ИТМО"], datetime(year=2020, month=1, day=1).date())
        self.assertIn("title6", map(lambda current_news: current_news.title, received_news))

    def test_get_news_by_one_university_and_last_date_not_suitable_news(self):
        received_news = self.db.get_news(["ИТМО"], datetime(year=2020, month=1, day=1).date())
        self.assertNotIn("title5", map(lambda current_news: current_news.title, received_news))

    def test_get_news_by_one_university_and_topics_suitable_news(self):
        received_news = self.db.get_news(["Политех"], topics=["Образование"])
        self.assertIn("title4", map(lambda current_news: current_news.title, received_news))

    def test_get_news_by_one_university_and_topics_not_suitable_news(self):
        received_news = self.db.get_news(["Политех"], topics=["Образование"])
        self.assertNotIn("title3", map(lambda current_news: current_news.title, received_news))

    def test_get_subscribed_users_to_send_news(self):
        self.db.set_sending_time(4, "M-10-17")
        self.db.set_universities(4, ["Политех"])
        users = self.db.get_subscribed_users_to_send_news(["M-10-17"], datetime.today())
        self.assertIn(4, map(lambda user: user.vk_id, users))

    def test_get_subscribed_users_to_send_news_not_suitable_user(self):
        self.db.set_sending_time(3, "M-10-17")
        self.db.set_universities(3, ["Политех"])
        self.db.set_sending_time(2, "M-10-16")
        self.db.set_universities(2, ["Политех"])
        users = self.db.get_subscribed_users_to_send_news(["M-10-17"], datetime.today())
        self.assertNotIn(2, map(lambda user: user.vk_id, users))

    def test_delete_user(self):
        self.db.add_user(7, 4)
        self.db.delete_users([7])
        self.assertFalse(self.db.is_user_exist(7))

    def test_delete_news(self):
        self.db.add_news(datetime.today().date(), "ИТМО", "title10", "https://1")
        self.db.delete_news(["title10"])
        received_news = self.db.get_news(["ИТМО"])
        self.assertNotIn("title10", map(lambda current_news: current_news.title, received_news))


if __name__ == '__main__':
    unittest.main()
