import json

# Local
from rpg.configs import CHARS_DATA_PATH, SHOW_SHEETS, HORIZONTRAL_SHEET_VIEW
from rpg.utils.sheet_view import display_character_sheet
from rpg.utils.auxiliar_func import cls, pause

from rpg.models.combat import CombatController
from rpg.models.character import Character

class RPGSystem:
    def __init__(self):
        self.characters: list[Character] = []
        self.combat_controller = CombatController()
        self._setup()

    def main(self):

        while True:
            if SHOW_SHEETS:
                self.show_characters()

            print('\n=== Actions ===')
            print('1) ...')
            print('2) Duel')
            print('0) Menu')
            print('q) Quit')
            opt = input('> ').lower()
            cls()

            match opt:
                case '1':
                    ...

                case '2':
                    self._simple_duel(self.characters[0], self.characters[1])

                case '0':
                    self._menu()

                case 'q':
                    break

                case _:
                    print('Invalid option, try again.')

    def show_characters(self):
        display_character_sheet(self.characters, HORIZONTRAL_SHEET_VIEW)

    def _setup(self):
        self._load_chars()
        pause('Started RPG System')

    def _simple_duel(self, first_att: Character, second_att: Character):
        self.combat_controller.simple_duel(first_att, second_att)
        cls()

    def _menu(self):
        global SHOW_SHEETS, HORIZONTRAL_SHEET_VIEW

        while True:
            if SHOW_SHEETS:
                self.show_characters()

            print('\n=== Menu Options ===')
            print(f'1) {'Show' if not SHOW_SHEETS else 'Hide'} Characters')
            print(f'2) Change Sheet View to {"Horizontal" if HORIZONTRAL_SHEET_VIEW else "Vertical"}')
            print('3) Save')
            print('q) Back')
            opt = input('> ').lower()
            cls()

            match opt:
                case '1':
                    SHOW_SHEETS = not SHOW_SHEETS
                    print('Characters visibility changed successfully.')

                case '2':
                    HORIZONTRAL_SHEET_VIEW = not HORIZONTRAL_SHEET_VIEW
                    print('Sheet view changed successfully.')

                case '3':
                    print('Saving characters...')
                    self._save_characters()
                    print('Characters saved successfully.')

                case 'q':
                    break

                case _:
                    print('Invalid option, try again.')

    def _save_characters(self, filepath: str = None):
        if filepath is None:
            filepath = CHARS_DATA_PATH

        arr = [char.to_dict() for char in self.characters]
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(arr, f, ensure_ascii=False, indent=2)
        
    def _load_chars(self, filepath: str = None) -> list[Character]:
        if filepath is None:
            filepath = CHARS_DATA_PATH

        data = json.load(open(filepath, 'r', encoding='utf-8'))
        # Se forem objetos gerados por to_dict(), talvez precise converter de volta.
        # Se forem objetos crus (mesmo formato de chars.json), basta usar Character(**data).
        self.characters = [Character(**char_data) for char_data in data]