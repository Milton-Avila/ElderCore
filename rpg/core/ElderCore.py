import json

# Local
from rpg.configs import CHARS_DATA_PATH, SETTINGS
from rpg.view.sheet_view import display_character_sheet
from rpg.utils.auxiliar_func import clear, pause

from rpg.models.classes import Duelist, Werebeast, Sorcerer
from rpg.combat.controller import CombatController
from rpg.models.character import Character

CLASS_MAP = {
    'dexterity': Duelist,
    'constitution': Werebeast,
    'intelligence': Sorcerer,
}

def load_characters_from_json(filepath: str = CHARS_DATA_PATH) -> list[Character]:
    def create_character(char_data: dict):
        main_attr = max(char_data['attributes'], key=char_data['attributes'].get)
        cls = CLASS_MAP.get(main_attr, Character)
        return cls(**char_data)

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return [create_character(char_data) for char_data in data]


def save_characters_to_json(characters: list[Character], filepath: str = CHARS_DATA_PATH):
    arr = [char.to_dict() for char in characters]
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(arr, f, ensure_ascii=False, indent=2)


class ElderCore:
    def __init__(self):
        self.characters: list[Character] = load_characters_from_json()
        self.combat_controller = CombatController()
        self.message = ''
        pause('Started ElderCore RPG!')

    def main(self):
        while True:
            clear()
            if SETTINGS['show_sheets']:
                self.show_characters()

            self._print_message()
            self._print_main_menu()

            opt = input('> ').lower()
            clear()

            match opt:
                case '1':
                    self._duel()
                case '0':
                    self._options_menu()
                case 'q':
                    break
                case _:
                    self._set_message('Invalid option, try again.')

    def show_characters(self):
        display_character_sheet(self.characters, SETTINGS['horizontal_view'])

    def _print_main_menu(self):
        print('\n=== Main Menu ===')
        print('1) Duel')
        print('...')
        print('0) Options')
        print('q) Quit')

    def _print_message(self):
        if self.message:
            print(self.message)

    def _set_message(self, message: str):
        self.message = message

    def _duel(self):
        from rpg.models.monsters.goblin import Goblin
        self.combat_controller.duel([self.characters[0], self.characters[1], self.characters[2]], [Goblin(), Goblin()])

    def _options_menu(self):
        while True:
            clear()
            if SETTINGS['show_sheets']:
                self.show_characters()

            self._print_message()
            self._print_options_menu()

            opt = input('> ').lower()
            clear()

            options = {
                '1': self._toggle_show_characters,
                '2': self._toggle_sheet_view,
                '0': self._save_characters,
                'q': lambda: self._set_message('Back to main menu.')
            }

            handler = options.get(opt, lambda: self._set_message('Invalid option, try again.'))
            handler()

            if opt == 'q':
                break

    def _print_options_menu(self):
        print('\n=== Options Menu ===')
        print(f"1) {'Show' if not SETTINGS['show_sheets'] else 'Hide'} Characters")
        print(f"2) Change Sheet View to {'Horizontal' if not SETTINGS['horizontal_view'] else 'Vertical'}")
        print('...')
        print('0) Save')
        print('q) Back')

    def _toggle_show_characters(self):
        SETTINGS['show_sheets'] = not SETTINGS['show_sheets']
        self._set_message('Characters visibility changed successfully.')

    def _toggle_sheet_view(self):
        SETTINGS['horizontal_view'] = not SETTINGS['horizontal_view']
        self._set_message('Sheet view changed successfully.')

    def _save_characters(self):
        save_characters_to_json(self.characters)
        self._set_message('Characters saved successfully.')
