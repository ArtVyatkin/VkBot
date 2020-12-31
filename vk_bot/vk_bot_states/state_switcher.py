from .initial_state import InitialState
from .waiting_state import WaitingState
from .simple_selection_state import SimpleSelectionState
from .event_handler import *
from .state_settings_for_ui import state_settings_for_ui


def get_state_switcher(vk_bot):
    eventHandler = EventHandler(vk_bot)
    return {
        VkStateTypes.INITIAL.value: InitialState(vk_bot),

        VkStateTypes.WAITING_STATE.value: WaitingState(vk_bot),

        VkStateTypes.SELECT_UNIVERSITY_ONE_TIME_GETTING_NEWS.value:
            SimpleSelectionState(vk_bot,
                                 eventHandler.get_handler_with_saving_payload(
                                     "selected_university",
                                     VkStateTypes.SELECT_TIME_FOR_ONE_TIME_GETTING_NEWS),
                                 **state_settings_for_ui["selection_of_university"]),
        VkStateTypes.SELECT_TIME_FOR_ONE_TIME_GETTING_NEWS.value:
            SimpleSelectionState(vk_bot,
                                 eventHandler.get_handler_with_saving_payload(
                                     "selected_time",
                                     VkStateTypes.SELECT_TOPIC_FOR_ONE_TIME_GETTING_NEWS),
                                 **state_settings_for_ui["selection_of_time_for_one_selection"],
                                 ),

        VkStateTypes.SELECT_TOPIC_FOR_ONE_TIME_GETTING_NEWS.value:
            SimpleSelectionState(vk_bot, eventHandler.handle_topic_selection_when_one_time_sending,
                                 **state_settings_for_ui["selection_of_topic"]),

        VkStateTypes.NEED_TO_SHOW_FOLLOWING_NEWS:
            SimpleSelectionState(vk_bot,
                                 eventHandler.handle_continued_news_showing,
                                 **state_settings_for_ui["selection_of_answer_to_continue_showing_news"]),

        VkStateTypes.ADD_TOPIC.value:
            SimpleSelectionState(vk_bot, eventHandler.handle_topic_adding,
                                 **state_settings_for_ui["selection_of_topic"]),

        VkStateTypes.SELECT_TIME_PERIOD.value:
            SimpleSelectionState(vk_bot, eventHandler.handle_time_period_selection,
                                 **state_settings_for_ui["selection_of_time_period"]),

        VkStateTypes.SELECT_TIME_OF_DAY.value:
            SimpleSelectionState(vk_bot, eventHandler.handle_time_of_day_selection,
                                 **state_settings_for_ui["selection_of_time_of_day"]),

        VkStateTypes.SELECT_DAY_OF_MONTH.value:
            SimpleSelectionState(vk_bot, eventHandler.handle_day_of_month_selection,
                                 **state_settings_for_ui["selection_of_day_of_month"]),

        VkStateTypes.SELECT_DAY_OF_WEEK.value:
            SimpleSelectionState(vk_bot, eventHandler.handle_day_of_week_selection,
                                 **state_settings_for_ui["selection_of_day_of_week"]),

        VkStateTypes.SUBSCRIPTION.value:
            SimpleSelectionState(vk_bot, eventHandler.handle_university_selection_when_subscribe,
                                 **state_settings_for_ui["selection_of_university"]),

        VkStateTypes.UNSUBSCRIPTION.value:
            SimpleSelectionState(vk_bot, eventHandler.handle_university_selection_when_unsubscribe,
                                 **state_settings_for_ui["selection_of_university_for_unsubscription"]),
    }
