from abc import abstractmethod


class State:
    def __init__(self, vk_bot):
        self.vk_bot = vk_bot

    def handle_unknown_event(self, event):
        self.vk_bot.send_message(event.user_id, "Моя тебя не понимать")

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def send(self, user_id):
        pass
