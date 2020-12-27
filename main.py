from datetime import datetime, timedelta

from vk_bot import VkBot
import logging
import threading
import schedule
import time


def vk_start(vk_bot1):
    logging.basicConfig(format='%(asctime)s %(name)s - %(levelname)s:%(message)s', level=logging.INFO)
    logging.info("Start")
    vk_bot1.run()


def send_news(vk_bot1):
    current_datetime = datetime.today() + timedelta(hours=1)
    possible_sending_time = [
        current_datetime.strftime('M-%d-%H'),
        current_datetime.strftime('W-%u-%H'),
        current_datetime.strftime('%H')
    ]

    users = vk_bot1.db.get_subscribed_users_to_send_news(possible_sending_time, current_datetime.date())
    for user in users:
        news = vk_bot1.db.get_news(user.universities, user.last_sending_date, user.topics)
        vk_bot.send_news_out_of_state_handling(user.vk_id, news)


def job3(vk_bot1):
    print("3 --- FROM SCHEDULE -- I'm running on thread %s" % threading.current_thread())


def start_schedule1(vk_bot1):
    schedule.every().minute.at(":00").do(send_news, vk_bot1)
    schedule.every().minute.at(":30").do(send_news, vk_bot1)
    while 1:
        print("!!!!")
        schedule.run_pending()
        time.sleep(5)


vk_bot = VkBot()

thread_for_schedule = threading.Thread(target=start_schedule1, args=(vk_bot,))
thread_for_schedule.start()

thread_for_bot = threading.Thread(target=vk_start, args=(vk_bot,))
thread_for_bot.start()
