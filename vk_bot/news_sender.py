from math import ceil

from vk_bot.carousel_making import get_carousel_from_news
from vk_bot.phrases import phrases
from vk_bot.vk_bot_states import VkStateTypes


class NewsSender:
    def __init__(self, vk_bot, max_number_of_news_for_one_sending):
        self.vk_bot = vk_bot
        self.max_number_of_news_for_one_sending = max_number_of_news_for_one_sending

    def post_processing_of_sending(self, user_id, news):
        if news.count() <= self.max_number_of_news_for_one_sending:
            self.vk_bot.set_state(user_id, VkStateTypes.WAITING_STATE.value, {"isFirst": False})
        else:
            not_shown_news = news.offset(self.max_number_of_news_for_one_sending)
            not_shown_news_ids = list(map(lambda current_news: current_news.id, not_shown_news))
            self.vk_bot.set_state(user_id, VkStateTypes.NEED_TO_SHOW_FOLLOWING_NEWS.value,
                                  {"not_shown_news": not_shown_news_ids})

    def send_news(self, user_id, news):
        if news.count() == 0:
            self.vk_bot.send_message(user_id, phrases["no_news"])
        else:
            if news.count() > self.max_number_of_news_for_one_sending:
                message = phrases["few_first_news"].format(self.max_number_of_news_for_one_sending)
            else:
                message = phrases["news"]

            news_to_show = news.limit(self.max_number_of_news_for_one_sending)
            for i in range(0, ceil(news_to_show.count() / 10)):
                self.vk_bot.send_message(user_id, message,
                                         template=get_carousel_from_news(news_to_show.offset(i * 10).limit(10)))
                message = phrases["continuation"]
        self.post_processing_of_sending(user_id, news)
