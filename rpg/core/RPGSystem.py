import json

# Local
from rpg.configs import CHARS_DATA_PATH, SHOW_SHEETS, HORIZONTRAL_SHEET_VIEW
from rpg.view.sheet_view import display_character_sheet
from rpg.utils.auxiliar_func import clear, pause

from rpg.models.classes import Duelist, Werebeast, Bard
from rpg.core.combat import CombatController
from rpg.models.character import Character

class RPGSystem:
    def __init__(self):
        self.characters: list[Character] = []
        self.combat_controller = CombatController()
        self._setup()

    def main(self):

        while True:
            clear()
            if SHOW_SHEETS:
                self.show_characters()

            self._show_menu_message()
            print('\n=== Menu ===')
            print('1) Duel')
            print('...')
            print('0) Options')
            print('q) Quit')
            opt = input('> ').lower()
            clear()

            match opt:
                case '1':
                    self._duel(self.characters[0], self.characters[2])

                case '2':
                    ...

                case '0':
                    self._menu()

                case 'q':
                    break

                case _:
                    self._set_menu_message('Invalid option, try again.')

    def show_characters(self):
        display_character_sheet(self.characters, HORIZONTRAL_SHEET_VIEW)
    
    def _show_menu_message(self):
        message = getattr(self, 'message', '')
        print(message)

    def _set_menu_message(self, message: str):
        self.message = message

    def _setup(self):
        self._load_chars()
        pause('Started RPG System!')

    def _duel(self, first_att: Character, second_att: Character):
        self.combat_controller.duel(first_att, second_att)

    def _menu(self):
        global SHOW_SHEETS, HORIZONTRAL_SHEET_VIEW

        while True:
            clear()

            if SHOW_SHEETS:
                self.show_characters()

            self._show_menu_message()
            print('\n=== Options Menu ===')
            print(f'1) {'Show' if not SHOW_SHEETS else 'Hide'} Characters')
            print(f'2) Change Sheet View to {"Horizontal" if HORIZONTRAL_SHEET_VIEW else "Vertical"}')
            print('...')
            print('0) Save')
            print('q) Back')
            opt = input('> ').lower()
            clear()

            match opt:
                case '1':
                    SHOW_SHEETS = not SHOW_SHEETS
                    self._set_menu_message('Characters visibility changed successfully.')

                case '2':
                    HORIZONTRAL_SHEET_VIEW = not HORIZONTRAL_SHEET_VIEW
                    self._set_menu_message('Sheet view changed successfully.')

                case '0':
                    print('Saving characters...')
                    self._save_characters()
                    self._set_menu_message('Characters saved successfully.')

                case 'q':
                    self._set_menu_message('Back to main menu.')
                    break

                case _:
                    self._set_menu_message('Invalid option, try again.')

    def _save_characters(self, filepath: str = None):
        if filepath is None:
            filepath = CHARS_DATA_PATH

        arr = [char.to_dict() for char in self.characters]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(arr, f, ensure_ascii=False, indent=2)

    def _load_chars(self, filepath: str = CHARS_DATA_PATH) -> list[Character]:
        CLASS_MAP = {
            'dexterity': Duelist,
            'strength': Werebeast,
            'charisma': Bard,
        }

        def create_character(char_data: dict):
            main_attr = max(char_data['attributes'], key=char_data['attributes'].get)
            cls = CLASS_MAP.get(main_attr, Character)
            return cls(**char_data)
        
        data = json.load(open(filepath, 'r', encoding='utf-8'))

        self.characters = [create_character(char_data) for char_data in data]

        