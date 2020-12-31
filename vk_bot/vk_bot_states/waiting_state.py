from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from vk_bot.phrases import phrases
from vk_bot.vk_bot_states import VkStateTypes
from .state import State


class WaitingState(State):
    def __init__(self, vk_bot):
        super().__init__(vk_bot)
        self.state_switcher = {
            phrases["one_time_getting_news"]: VkStateTypes.SELECT_UNIVERSITY_ONE_TIME_GETTING_NEWS,
            phrases["add_topic"]: VkStateTypes.ADD_TOPIC,
            phrases["subscribe"]: VkStateTypes.SUBSCRIPTION,
            phrases["unsubscribe"]: VkStateTypes.UNSUBSCRIPTION,
            phrases["change_time"]: VkStateTypes.SELECT_TIME_PERIOD,
        }

    def get_keyboard(self, user_id):
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button(phrases["one_time_getting_news"], color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(phrases["subscribe"], color=VkKeyboardColor.POSITIVE)
        if self.vk_bot.has_user_subscription(user_id):
            keyboard.add_button(phrases["unsubscribe"], color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()
            keyboard.add_button(phrases["change_time"], color=VkKeyboardColor.SECONDARY)
            keyboard.add_button(phrases["add_topic"], color=VkKeyboardColor.SECONDARY)
        return keyboard.get_keyboard()

    def send(self, user_id):
        if self.vk_bot.get_state_payload(user_id)["isFirst"]:
            message = phrases["message_for_first_interaction"]
        else:
            message = phrases["message_to_re_interact"]

        self.vk_bot.send_message(user_id, message, keyboard=self.get_keyboard(user_id))

    def handle_event(self, event):
        if event.text in self.state_switcher:
            self.vk_bot.set_state(event.user_id, self.state_switcher[event.text])
        else:
            self.handle_unknown_event(event)
