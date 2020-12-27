from vk_api.keyboard import VkKeyboard

from .state import State


class SimpleSelectionState(State):
    def __init__(self, vk_bot, on_selecting, phrases_to_choose, introductory_phrase, number_of_elements_in_row,
                 allowed_values=None, colors=None):
        super().__init__(vk_bot)
        self.on_selecting = on_selecting
        self.phrases_to_choose = phrases_to_choose
        self.introductory_phrase = introductory_phrase
        self.number_of_elements_in_row = number_of_elements_in_row

        if allowed_values is None:
            self.allowed_values = phrases_to_choose
        else:
            self.allowed_values = allowed_values

        if colors is None:
            self.colors = {}
        else:
            self.colors = colors

    def add_button(self, keyboard, index):
        if index in self.colors.keys():
            keyboard.add_button(self.phrases_to_choose[index], self.colors[index])
        else:
            keyboard.add_button(self.phrases_to_choose[index])

    def add_keyboard_line(self, keyboard, start_index):
        end_index = start_index + self.number_of_elements_in_row
        number_of_all_phrases = len(self.phrases_to_choose)
        if end_index > number_of_all_phrases:
            end_index = number_of_all_phrases
        for index in range(start_index, end_index):
            self.add_button(keyboard, index)

    def get_keyboard(self):
        keyboard = VkKeyboard(inline=True)
        self.add_keyboard_line(keyboard, 0)
        for index in range(self.number_of_elements_in_row, len(self.phrases_to_choose),
                           self.number_of_elements_in_row):
            keyboard.add_line()
            self.add_keyboard_line(keyboard, index)
        return keyboard.get_keyboard()

    def send(self, user_id):
        self.vk_bot.send_message(user_id, self.introductory_phrase, keyboard=self.get_keyboard())

    def handle_event(self, event):
        if event.text in self.allowed_values:
            self.on_selecting(event)
        else:
            self.handle_unknown_event(event)
