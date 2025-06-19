import json

# Local
from rpg.configs import CHARS_DATA_PATH, SETTINGS
from rpg.utils.auxiliar_func import clear_console, slow_write, pause
from rpg.view.sheet_view import display_character_sheet
from rpg.combat.loop import CombatLoop

# Models
from rpg.models.characters import Duelist, Werebeast, Healer
from rpg.models.characters.character import Character

CLASS_MAP = {
    'dexterity':Duelist,
    'constitution':Werebeast,
    'wisdom':Healer,
}

def load_characters_from_json(filepath:str = CHARS_DATA_PATH) -> list[Character]:
    def create_character(char_data:dict):
        main_attr = max(
            char_data['attrs_data'],
            key=char_data['attrs_data'].get
        )

        return CLASS_MAP.get(main_attr, Character)(
            **char_data
        )

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return [create_character(char_data) for char_data in data]

def save_characters_to_json(
        characters:list[Character],
        filepath:str = CHARS_DATA_PATH
    ):

    arr = [char.to_dict() for char in characters]
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(arr, f, ensure_ascii=False, indent=2)


class ElderCore:
    def __init__(self):
        self.characters:list[Character] = load_characters_from_json()
        self.combat_controller = CombatLoop()
        pause('Started ElderCore RPG!', enter_to_continue=True)

    def main(self) -> None:
        while True:
            opt = self._show_menu('main')
            if opt == 'q':
                break

    def _show_menu(self, menu_type:str) -> str:
        self.__show_message()

        # Char-Sheet
        if SETTINGS['show_sheets']:
            display_character_sheet(
                self.characters, SETTINGS['horizontal_view']
            )

        # Options
        menus = {
            'main': {
                'title': 'Main Menu',
                'options': {
                    '1': ('Fight', self._fight),
                    '0': ('Options', lambda: self._show_menu('options')),
                    'q': ('Quit', lambda: slow_write('Goodbye adventurer.')),
                }
            },
            'options': {
                'title': 'Options Menu',
                'options': {
                    '1': (f"{'Show' if not SETTINGS['show_sheets'] else 'Hide'} Characters", 
                          self._toggle_show_characters),
                    '2': (f"Change Sheet View to {'Horizontal' if not SETTINGS['horizontal_view'] else 'Vertical'}", 
                          self._toggle_sheet_view),
                    '0': ('Save Characters', self._save_characters),
                    'q': ('Back to Main Menu', lambda: None),
                }
            }
        }

        # Menu
        menu = menus[menu_type]
        print(f"\n=== {menu['title']} ===")
        for key, (desc, _) in menu['options'].items():
            if key == '0':
                print('-')
            print(f"{key}) {desc}")

        # Input
        opt = ''
        while opt is '':
            opt = input('> ').lower().strip()
        clear_console()
        
        if opt == '':
            return
        
        menu['options'].get(opt, (
            'Invalid option', 
            lambda: self.__set_message('Invalid option, try again.')
        ))[1]()

        return opt

    def _fight(self):
        from rpg.models.monsters.goblin import Goblin
        self.combat_controller.battle(
            [self.characters[0], self.characters[1], self.characters[2]],
            [Goblin(), Goblin()]
        )

    def _toggle_show_characters(self):
        SETTINGS['show_sheets'] = not SETTINGS['show_sheets']
        self.__set_message('Characters visibility changed successfully.')

    def _toggle_sheet_view(self):
        SETTINGS['horizontal_view'] = not SETTINGS['horizontal_view']
        self.__set_message('Sheet view changed successfully.')

    def _save_characters(self):
        save_characters_to_json(self.characters)
        self.__set_message('Characters saved successfully.')

    def __show_message(self):
        pause(SETTINGS['message'], delay=0.015)
        self.__set_message('')

    def __set_message(self, message:str):
        SETTINGS['message'] = message