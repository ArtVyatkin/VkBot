from datetime import timedelta, date

from vk_bot.phrases import phrases
from .vk_state_types import VkStateTypes
from .state_settings_for_ui import days_of_week


class EventHandler:
    def __init__(self, vk_bot):
        self.vk_bot = vk_bot

    def handle_topic_adding(self, event):
        topics = self.vk_bot.db.get_topics(event.user_id)
        if event.text == phrases["any_topic"]:
            topics = []
            self.vk_bot.db.set_topics(event.user_id, topics)
            message = phrases["any_topic_success"]
        elif event.text not in topics:
            topics += [event.text]
            self.vk_bot.db.set_topics(event.user_id, topics)
            message = phrases["add_topic_success"]
        else:
            message = phrases["add_topic_failure"]
        self.vk_bot.send_message(event.user_id, message)
        self.vk_bot.set_state(event.user_id, VkStateTypes.WAITING_STATE.value, {"isFirst": False})

    def handle_continued_news_showing(self, event):
        if event.text == phrases["yes"]:
            payload = self.vk_bot.get_state_payload(event.user_id)
            news = self.vk_bot.db.get_news_by_ids(payload["not_shown_news"])
            self.vk_bot.news_sender.send_news(event.user_id, news)
        elif event.text == phrases["no"]:
            self.vk_bot.set_state(event.user_id, VkStateTypes.WAITING_STATE.value, {"isFirst": False})

    def get_handler_with_saving_payload(self, payload_property_name, next_state):
        def handle_event(self, event):
            payload = self.vk_bot.get_state_payload(event.user_id)
            payload.update({payload_property_name: event.text})
            self.vk_bot.set_state(event.user_id, next_state.value, payload)

        return handle_event

    def handle_university_selection_when_subscribe(self, event):
        universities = self.vk_bot.db.get_user(event.user_id).universities
        if event.text not in universities:
            universities += [event.text]
            self.vk_bot.db.set_universities(event.user_id, universities)
            self.vk_bot.set_state(event.user_id, VkStateTypes.SELECT_TIME_PERIOD.value)
        else:
            self.vk_bot.send_message(event.user_id, phrases["subscribe_failure"])
            self.vk_bot.set_state(event.user_id, VkStateTypes.WAITING_STATE.value, {"isFirst": False})

    def handle_time_of_day_selection(self, event):
        payload = self.vk_bot.get_state_payload(event.user_id)
        self.vk_bot.db.set_sending_time(event.user_id, payload["sending_time"] + event.text[:-3])
        self.vk_bot.set_state(event.user_id, VkStateTypes.WAITING_STATE.value, {"isFirst": False})

    def handle_time_period_selection(self, event):
        if event.text == phrases["once_a_day"]:
            sending_time = ""
            next_state = VkStateTypes.SELECT_TIME_OF_DAY
        elif event.text == phrases["once_a_week"]:
            sending_time = "W-"
            next_state = VkStateTypes.SELECT_DAY_OF_WEEK
        else:
            sending_time = "M-"
            next_state = VkStateTypes.SELECT_DAY_OF_MONTH
        self.vk_bot.set_state(event.user_id, next_state.value, {"sending_time": sending_time})

    def handle_day_of_month_selection(self, event):
        payload = self.vk_bot.get_state_payload(event.user_id)
        self.vk_bot.set_state(event.user_id, VkStateTypes.SELECT_TIME_OF_DAY.value,
                              {"sending_time": payload["sending_time"] + event.text + "-"})

    def handle_day_of_week_selection(self, event):
        payload = self.vk_bot.get_state_payload(event.user_id)
        self.vk_bot.set_state(event.user_id, VkStateTypes.SELECT_TIME_OF_DAY.value,
                              {"sending_time": payload["sending_time"] + str(days_of_week.index(event.text) + 1) + "-"})

    def handle_university_selection_when_unsubscribe(self, event):
        universities = self.vk_bot.db.get_user(event.user_id).universities
        if event.text == phrases["unsubscribe_from_everything"]:
            self.vk_bot.db.set_universities(event.user_id, [])
            message = phrases["unsubscribe_from_everything_success"]
        elif event.text in universities:
            universities.remove(event.text)
            self.vk_bot.db.set_universities(event.user_id, universities)
            message = phrases["unsubscribe_success"]
        else:
            message = phrases["unsubscribe_failure"]
        self.vk_bot.send_message(event.user_id, message)
        self.vk_bot.set_state(event.user_id, VkStateTypes.WAITING_STATE.value, {"isFirst": False})

    def handle_topic_selection_when_one_time_sending(self, event):
        payload = self.vk_bot.get_state_payload(event.user_id)
        if payload["selected_time"] == phrases["for_last_day"]:
            last_time = date.today()
        elif payload["selected_time"] == phrases["for_last_week"]:
            last_time = date.today() - timedelta(days=7)
        elif payload["selected_time"] == phrases["for_last_month"]:
            last_time = date.today() - timedelta(days=31)
        elif payload["selected_time"] == phrases["over_past_six_months"]:
            last_time = date.today() - timedelta(days=182)
        else:
            last_time = date.today()

        if event.text == phrases["any_topic"]:
            topics = None
        else:
            topics = [event.text]
        news = self.vk_bot.db.get_news([payload["selected_university"]], last_time, topics)
        self.vk_bot.send_news(event.user_id, news)
