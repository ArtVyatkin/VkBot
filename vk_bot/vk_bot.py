import json
import random
import vk_api
import requests
from ast import literal_eval
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkUpload
from database import Database
from .image_handler import ImageHandler
from .news_sender import NewsSender
from .vk_bot_states import VkStateTypes, get_state_switcher


class VkBot:
    def __init__(self):
        with open('config.json') as config_file:
            vk_bot_config = json.loads(config_file.read())['vk_bot']
        self.state = None
        self.session = requests.Session()
        vk_session = vk_api.VkApi(token=vk_bot_config['token'])
        self.longpoll = VkLongPoll(vk_session)
        self.vk = vk_session.get_api()
        self.upload = VkUpload(vk_session)
        self.db = Database()
        self.news_sender = NewsSender(self, 50)
        self.image_handler = ImageHandler(self)
        self.state_switcher = get_state_switcher(self)

    def send_news_out_of_state_handling(self, user_id, news):
        self.news_sender.send_news(user_id, news)
        self.state.send(user_id)

    def send_news(self, user_id, news):
        self.news_sender.send_news(user_id, news)

    def has_user_subscription(self, user_id):
        return len(self.db.get_user(user_id).universities) != 0

    def set_state_to_db(self, user_id, state_id, state_payload=None):
        if state_payload is not None:
            state_payload = str(state_payload)
        self.db.set_user_state(user_id, state_id, state_payload)

    def set_state(self, user_id, state_id, state_payload=None):
        self.set_state_to_db(user_id, state_id, state_payload)
        self.set_state_to_vk_bot(state_id)

    def set_state_to_vk_bot(self, state_id):
        self.state = self.state_switcher[state_id]

    def get_state_payload(self, user_id):
        return literal_eval(self.db.get_user(user_id).state_payload)

    def set_state_payload(self, user_id, state_payload):
        return self.db.set_user_state_payload(user_id, str(state_payload))

    def send_message(self, user_id, message="", template=None, keyboard=None):
        if template is None:
            template = {}
        self.vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=random.randint(0, 4294967290),
            template=template,
            keyboard=keyboard
        )

    def run(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                user_id = event.user_id
                if not self.db.is_user_exist(user_id):
                    self.db.add_user(user_id, VkStateTypes.INITIAL.value)
                    self.set_state_to_vk_bot(VkStateTypes.INITIAL.value)
                else:
                    current_state = self.db.get_user(user_id).state
                    self.set_state_to_vk_bot(current_state)
                self.state.handle_event(event)
                self.state.send(event.user_id)
