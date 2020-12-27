from vk_api.keyboard import VkKeyboard

from .vk_state_types import VkStateTypes
from .state import State
from vk_bot.phrases import phrases


class InitialState(State):
    def __init__(self, vk_bot):
        super().__init__(vk_bot)

    def send(self, user_id):
        self.vk_bot.send_message(user_id, phrases["greeting"], keyboard=VkKeyboard.get_empty_keyboard())

    def handle_event(self, event):
        if event.text == phrases["to_begin"]:
            self.send(event.user_id)
            self.vk_bot.set_state(event.user_id, VkStateTypes.WAITING_STATE.value, {"isFirst": True})
        else:
            self.handle_unknown_event(event)
