from datetime import datetime, timedelta

from vk_bot import VkBot
import threading
import schedule
import time

vk_bot = VkBot()


def vk_start():
    vk_bot.run()


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


def start_schedule(vk_bot1):
    schedule.every().hour.at(":00").do(send_news, vk_bot1)
    while 1:
        schedule.run_pending()
        time.sleep(10000)


thread_for_schedule = threading.Thread(target=start_schedule, args=(vk_bot,))
thread_for_schedule.start()

thread_for_bot = threading.Thread(target=vk_start, args=(vk_bot,))
thread_for_bot.start()
