from datetime import datetime, timedelta

from vk_bot import VkBot
import threading
import schedule
import time
from news_adding import set_news_data
from crawlers import SPbSUCrawler, ITMOCrawler, PolitehCrawler


vk_bot = VkBot()


def vk_start():
    vk_bot.run()


def set_new_news_to_database():
    start_date = datetime.today() - timedelta(days=1)
    set_news_data(vk_bot, SPbSUCrawler, start_date, "СПбГУ")
    set_news_data(vk_bot, ITMOCrawler, start_date, "ИТМО")
    set_news_data(vk_bot, PolitehCrawler, start_date, "Политех")


def send_news():
    current_datetime = datetime.today() + timedelta(hours=1)
    possible_sending_time = [
        current_datetime.strftime('M-%d-%H'),
        current_datetime.strftime('W-%u-%H'),
        current_datetime.strftime('%H')
    ]

    users = vk_bot.db.get_subscribed_users_to_send_news(possible_sending_time, current_datetime.date())
    for user in users:
        news = vk_bot.db.get_news(user.universities, user.last_sending_date, user.topics)
        vk_bot.send_news_out_of_state_handling(user.vk_id, news)


def start_schedule():
    schedule.every().hour.at(":00").do(send_news)
    schedule.every().hour.at(":30").do(set_new_news_to_database)
    while True:
        schedule.run_pending()
        time.sleep(30)


thread_for_schedule = threading.Thread(target=start_schedule)
thread_for_schedule.start()

thread_for_bot = threading.Thread(target=vk_start)
thread_for_bot.start()
