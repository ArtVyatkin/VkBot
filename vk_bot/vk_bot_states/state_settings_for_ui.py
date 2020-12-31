from vk_api.keyboard import VkKeyboardColor

from crawlers import available_universities
from vk_bot.phrases import phrases

topics_settings = [
    phrases["university_achievements"],
    phrases["students_achievements"],
    phrases["education"],
    phrases["cooperation"],
    phrases["university_life"],
    phrases["science"],
    phrases["official_documents"],
    phrases["miscellanea"],
    phrases["any_topic"],
]

days_of_week = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье"
]

state_settings_for_ui = {
    "selection_of_university": {
        "phrases_to_choose": available_universities,
        "introductory_phrase": phrases["select_university"],
        "number_of_elements_in_row": 1,
    },
    "selection_of_topic": {
        "phrases_to_choose": topics_settings,
        "introductory_phrase": phrases["select_topic"],
        "number_of_elements_in_row": 2,
        "colors": {8: VkKeyboardColor.PRIMARY},
    },
    "selection_of_time_for_one_selection": {
        "phrases_to_choose": [
            phrases["for_last_day"],
            phrases["for_last_week"],
            phrases["for_last_month"],
            phrases["over_past_six_months"],
        ],
        "introductory_phrase": phrases["select_time_period"],
        "number_of_elements_in_row": 1,
    },
    "selection_of_answer_to_continue_showing_news": {
        "phrases_to_choose": [
            phrases["yes"],
            phrases["no"],
        ],
        "introductory_phrase": phrases["question_of_continuing_to_show_news"],
        "number_of_elements_in_row": 2,
        "colors": {0: VkKeyboardColor.POSITIVE, 1: VkKeyboardColor.NEGATIVE},
    },
    "selection_of_time_period": {
        "phrases_to_choose": [
            phrases["once_a_day"],
            phrases["once_a_week"],
            phrases["once_a_month"],
        ],
        "introductory_phrase": phrases["select_period"],
        "number_of_elements_in_row": 1,
    },
    "selection_of_time_of_day": {
        "phrases_to_choose": [str(i) + ":00" for i in range(7, 22, 2)],
        "allowed_values": [str(i) + ":00" for i in range(0, 24)],
        "introductory_phrase": phrases["select_time_of_day"],
        "number_of_elements_in_row": 4,
    },
    "selection_of_day_of_month": {
        "phrases_to_choose": [1] + [i for i in range(5, 26, 5)] + [31],
        "allowed_values": [str(i) for i in range(1, 32)],
        "introductory_phrase": phrases["select_day_of_month"],
        "number_of_elements_in_row": 2,
    },
    "selection_of_day_of_week": {
        "phrases_to_choose": days_of_week,
        "introductory_phrase": phrases["select_day_of_week"],
        "number_of_elements_in_row": 2,
    },
    "selection_of_university_for_unsubscription": {
        "phrases_to_choose": available_universities + [phrases["unsubscribe_from_everything"]],
        "introductory_phrase": phrases["select_university"],
        "number_of_elements_in_row": 1,
        "colors": {len(available_universities): VkKeyboardColor.NEGATIVE},
    }
}
