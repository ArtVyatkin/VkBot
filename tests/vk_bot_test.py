import json
import unittest
from unittest import TestCase, mock
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_bot import VkBot
from vk_bot.phrases import phrases
from vk_bot.vk_bot_states import VkStateTypes
from vk_bot.vk_bot_states.state_settings_for_ui import state_settings_for_ui

USER_ID = 0


class SimulatedEvent:
    type = VkEventType.MESSAGE_NEW
    to_me = True

    def __init__(self, user_id, text):
        self.user_id = user_id
        self.text = text


def get_simulated_events(list_of_messages):
    return map(lambda message: SimulatedEvent(USER_ID, message), list_of_messages)


def get_labels_from_mocked_send_message(mocked_send_message):
    keyboard = json.loads(mocked_send_message.call_args[1]["keyboard"])
    labels = set()
    for row in keyboard["buttons"]:
        for button in row:
            labels.add(button["action"]["label"])
    return labels


def get_mocked_longpoll_listen(list_of_phrases):
    return mock.patch.object(VkLongPoll, 'listen',
                             return_value=get_simulated_events(list_of_phrases))


def get_phrases_to_choose(state_settings_identifier):
    return set(state_settings_for_ui[state_settings_identifier]["phrases_to_choose"])


class BaseVkBotTestClass(TestCase):
    vk_bot = None

    @classmethod
    def setUp(cls):
        cls.vk_bot = VkBot()

    @classmethod
    def tearDown(cls):
        cls.vk_bot.db.delete_users([USER_ID])


class InitialStateTests(BaseVkBotTestClass):
    def test_check_keyboard(self):
        with get_mocked_longpoll_listen([phrases["to_begin"]]):
            with mock.patch('vk_bot.VkBot.send_message') as mocked_send_message:
                self.vk_bot.run()
                self.assertEqual({phrases["subscribe"], phrases["one_time_getting_news"]},
                                 get_labels_from_mocked_send_message(mocked_send_message))

    def test_check_db_state(self):
        with get_mocked_longpoll_listen([phrases["to_begin"]]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual(VkStateTypes.WAITING_STATE.value, self.vk_bot.db.get_user(USER_ID).state)

    def test_incorrect_input_check_state(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], "dddfffddd"]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual(VkStateTypes.WAITING_STATE.value, self.vk_bot.db.get_user(USER_ID).state)

    def test_incorrect_input_check_keyboard(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], "12312321"]):
            with mock.patch('vk_bot.VkBot.send_message') as mocked_send_message:
                self.vk_bot.run()
                self.assertEqual({phrases["subscribe"], phrases["one_time_getting_news"]},
                                 get_labels_from_mocked_send_message(mocked_send_message))


class OneTimeGettingNewsTests(BaseVkBotTestClass):
    def test_select_university_state_check_keyboard(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["one_time_getting_news"]]):
            with mock.patch('vk_bot.VkBot.send_message') as mocked_send_message:
                self.vk_bot.run()
                self.assertEqual(get_phrases_to_choose("selection_of_university"),
                                 get_labels_from_mocked_send_message(mocked_send_message))

    def test_select_university_state_check_db_state(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["one_time_getting_news"]]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual(VkStateTypes.SELECT_UNIVERSITY_ONE_TIME_GETTING_NEWS.value,
                                 self.vk_bot.db.get_user(USER_ID).state)

    def test_select_time_state_check_keyboard(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["one_time_getting_news"], "ИТМО"]):
            with mock.patch('vk_bot.VkBot.send_message') as mocked_send_message:
                self.vk_bot.run()
                self.assertEqual(get_phrases_to_choose("selection_of_time_for_one_selection"),
                                 get_labels_from_mocked_send_message(mocked_send_message))

    def test_select_time_state_check_db_state(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["one_time_getting_news"], "СПбГУ"]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual(VkStateTypes.SELECT_TIME_FOR_ONE_TIME_GETTING_NEWS.value,
                                 self.vk_bot.db.get_user(USER_ID).state)

    def test_select_topic_state_check_keyboard(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["one_time_getting_news"], "ИТМО",
                                         phrases["for_last_day"]]):
            with mock.patch('vk_bot.VkBot.send_message') as mocked_send_message:
                self.vk_bot.run()
                self.assertEqual(get_phrases_to_choose("selection_of_topic"),
                                 get_labels_from_mocked_send_message(mocked_send_message))

    def test_select_topic_state_check_db_state(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["one_time_getting_news"], "Политех",
                                         phrases["for_last_week"]]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual(VkStateTypes.SELECT_TOPIC_FOR_ONE_TIME_GETTING_NEWS.value,
                                 self.vk_bot.db.get_user(USER_ID).state)


class SubscriptionTests(BaseVkBotTestClass):
    def test_select_university_state_check_keyboard(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"]]):
            with mock.patch('vk_bot.VkBot.send_message') as mocked_send_message:
                self.vk_bot.run()
                self.assertEqual(get_phrases_to_choose("selection_of_university"),
                                 get_labels_from_mocked_send_message(mocked_send_message))

    def test_select_university_state_check_db_state(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"]]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual(VkStateTypes.SUBSCRIPTION.value,
                                 self.vk_bot.db.get_user(USER_ID).state)

    def test_select_time_period_state_check_keyboard(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "ИТМО"]):
            with mock.patch('vk_bot.VkBot.send_message') as mocked_send_message:
                self.vk_bot.run()
                self.assertEqual(get_phrases_to_choose("selection_of_time_period"),
                                 get_labels_from_mocked_send_message(mocked_send_message))

    def test_select_time_period_state_check_db_state(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "Политех"]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual(VkStateTypes.SELECT_TIME_PERIOD.value,
                                 self.vk_bot.db.get_user(USER_ID).state)

    def test_check_subscribed_universities_after_one_selection(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "Политех"]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual(["Политех"],
                                 self.vk_bot.db.get_user(USER_ID).universities)

    def test_select_day_of_month_state_check_keyboard(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "ИТМО", phrases["once_a_month"]]):
            with mock.patch('vk_bot.VkBot.send_message') as mocked_send_message:
                self.vk_bot.run()
                self.assertEqual(get_phrases_to_choose("selection_of_day_of_month"),
                                 get_labels_from_mocked_send_message(mocked_send_message))

    def test_select_day_of_month_state_check_db_state(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "ИТМО", phrases["once_a_month"]]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual(VkStateTypes.SELECT_DAY_OF_MONTH.value,
                                 self.vk_bot.db.get_user(USER_ID).state)

    def test_select_day_of_week_state_check_keyboard(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "Политех", phrases["once_a_week"]]):
            with mock.patch('vk_bot.VkBot.send_message') as mocked_send_message:
                self.vk_bot.run()
                self.assertEqual(get_phrases_to_choose("selection_of_day_of_week"),
                                 get_labels_from_mocked_send_message(mocked_send_message))

    def test_select_day_of_week_state_check_db_state(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "СПбГУ", phrases["once_a_week"]]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual(VkStateTypes.SELECT_DAY_OF_WEEK.value,
                                 self.vk_bot.db.get_user(USER_ID).state)

    def test_select_time_of_day_state_check_keyboard(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "Политех", phrases["once_a_day"]]):
            with mock.patch('vk_bot.VkBot.send_message') as mocked_send_message:
                self.vk_bot.run()
                self.assertEqual(get_phrases_to_choose("selection_of_time_of_day"),
                                 get_labels_from_mocked_send_message(mocked_send_message))

    def test_select_time_of_day_state_check_db_state(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "СПбГУ", phrases["once_a_day"]]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual(VkStateTypes.SELECT_TIME_OF_DAY.value,
                                 self.vk_bot.db.get_user(USER_ID).state)

    def test_select_daily_sending_check_time_in_db(self):
        with get_mocked_longpoll_listen(
                [phrases["to_begin"], phrases["subscribe"], "СПбГУ", phrases["once_a_day"], "11:00"]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual("11", self.vk_bot.db.get_user(USER_ID).sending_time)

    def test_select_weekly_sending_check_time_in_db(self):
        with get_mocked_longpoll_listen(
                [phrases["to_begin"], phrases["subscribe"], "СПбГУ", phrases["once_a_week"], "Вторник", "12:00"]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual("W-2-12", self.vk_bot.db.get_user(USER_ID).sending_time)

    def test_select_monthly_sending_check_time_in_db(self):
        with get_mocked_longpoll_listen(
                [phrases["to_begin"], phrases["subscribe"], "СПбГУ", phrases["once_a_month"], "7", "23:00"]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual("M-7-23", self.vk_bot.db.get_user(USER_ID).sending_time)

    def test_select_monthly_sending_wrong_input(self):
        with get_mocked_longpoll_listen(
                [phrases["to_begin"], phrases["subscribe"], "СПбГУ", phrases["once_a_month"], "100"]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual(VkStateTypes.SELECT_DAY_OF_MONTH.value,
                                 self.vk_bot.db.get_user(USER_ID).state)

    def test_select_daily_sending_wrong_input(self):
        with get_mocked_longpoll_listen(
                [phrases["to_begin"], phrases["subscribe"], "СПбГУ", phrases["once_a_day"], "13:30"]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual(VkStateTypes.SELECT_TIME_OF_DAY.value,
                                 self.vk_bot.db.get_user(USER_ID).state)

    def test_after_subscription_check_db_state(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "СПбГУ", phrases["once_a_month"],
                                         "7", "23:00"]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual(VkStateTypes.WAITING_STATE.value,
                                 self.vk_bot.db.get_user(USER_ID).state)

    def test_after_subscription_check_keyboard(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "СПбГУ", phrases["once_a_month"],
                                         "7", "23:00"]):
            with mock.patch('vk_bot.VkBot.send_message') as mocked_send_message:
                self.vk_bot.run()
                self.assertEqual({phrases["subscribe"], phrases["one_time_getting_news"], phrases["unsubscribe"],
                                  phrases["change_time"], phrases["add_topic"]},
                                 get_labels_from_mocked_send_message(mocked_send_message))


class ChangeTimeTests(BaseVkBotTestClass):
    def test_check_time_in_db(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "СПбГУ", phrases["once_a_month"],
                                         "7", "23:00", phrases["change_time"], phrases["once_a_week"], "Вторник",
                                         "10:00"]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual("W-2-10", self.vk_bot.db.get_user(USER_ID).sending_time)


class UnsubscriptionTests(BaseVkBotTestClass):
    def test_check_keyboard(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "Политех", phrases["once_a_month"],
                                         "13", "17:00", phrases["unsubscribe"]]):
            with mock.patch('vk_bot.VkBot.send_message') as mocked_send_message:
                self.vk_bot.run()
                self.assertEqual(get_phrases_to_choose("selection_of_university_for_unsubscription"),
                                 get_labels_from_mocked_send_message(mocked_send_message))

    def test_check_state(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "Политех", phrases["once_a_month"],
                                         "13", "17:00", phrases["unsubscribe"]]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual(VkStateTypes.UNSUBSCRIPTION.value,
                                 self.vk_bot.db.get_user(USER_ID).state)

    def test_check_subscribed_universities(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "Политех", phrases["once_a_month"],
                                         "13", "17:00", phrases["unsubscribe"], "Политех"]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual([], self.vk_bot.db.get_user(USER_ID).universities)

    def test_after_unsubscribe_all_universities_check_keyboard(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "Политех", phrases["once_a_month"],
                                         "13", "17:00", phrases["subscribe"], "СПбГУ", phrases["once_a_week"],
                                         "Четверг", "12:00", phrases["unsubscribe"],
                                         phrases["unsubscribe_from_everything"]]):
            with mock.patch('vk_bot.VkBot.send_message') as mocked_send_message:
                self.vk_bot.run()
                self.assertEqual({phrases["subscribe"], phrases["one_time_getting_news"]},
                                 get_labels_from_mocked_send_message(mocked_send_message))

    def test_unsubscribe_all_universities(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "Политех", phrases["once_a_month"],
                                         "13", "17:00", phrases["subscribe"], "СПбГУ", phrases["once_a_week"],
                                         "Четверг", "12:00", phrases["unsubscribe"],
                                         phrases["unsubscribe_from_everything"]]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual([], self.vk_bot.db.get_user(USER_ID).universities)


class AddingTopicsTests(BaseVkBotTestClass):
    def test_check_keyboard(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "Политех", phrases["once_a_month"],
                                         "13", "17:00", phrases["add_topic"]]):
            with mock.patch('vk_bot.VkBot.send_message') as mocked_send_message:
                self.vk_bot.run()
                self.assertEqual(get_phrases_to_choose("selection_of_topic"),
                                 get_labels_from_mocked_send_message(mocked_send_message))

    def test_check_db_state(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "Политех", phrases["once_a_month"],
                                         "13", "17:00", phrases["add_topic"]]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual(VkStateTypes.ADD_TOPIC.value,
                                 self.vk_bot.db.get_user(USER_ID).state)

    def test_check_topics_in_db(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "Политех", phrases["once_a_month"],
                                         "13", "17:00", phrases["add_topic"], phrases["education"]]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual([phrases["education"]], self.vk_bot.db.get_user(USER_ID).topics)

    def test_adding_several_topics(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "Политех", phrases["once_a_month"],
                                         "13", "17:00", phrases["add_topic"], phrases["education"],
                                         phrases["add_topic"], phrases["science"]]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual({phrases["education"], phrases["science"]},
                                 set(self.vk_bot.db.get_user(USER_ID).topics))

    def test_select_all_topics(self):
        with get_mocked_longpoll_listen([phrases["to_begin"], phrases["subscribe"], "Политех", phrases["once_a_month"],
                                         "13", "17:00", phrases["add_topic"], phrases["education"],
                                         phrases["add_topic"], phrases["science"], phrases["add_topic"],
                                         phrases["any_topic"]]):
            with mock.patch('vk_bot.VkBot.send_message'):
                self.vk_bot.run()
                self.assertEqual([], self.vk_bot.db.get_user(USER_ID).topics)


if __name__ == '__main__':
    unittest.main()
