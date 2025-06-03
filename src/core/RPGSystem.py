import json
import os

# Local
from src.configs import CHARS_DATA_PATH, HORIZONTRAL_SHEET_VIEW
from src.utils.sheet_view import display_character_sheet
from src.models.character import Character
from src.core.combat import simple_duel

class RPGSystem:
    def __init__(self):
        self.characters: list[Character] = []
        self._setup()

    def main_menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        while True:
            print("\n=== Main Menu ===")
            print("1) Show Characters")
            print("2) Duel")
            print("q) Sair")
            opt = input("> ").lower()

            if opt == "1":
                os.system('cls' if os.name == 'nt' else 'clear')
                self.show_characters()
                

            elif opt == "2":
                os.system('cls' if os.name == 'nt' else 'clear')
                simple_duel(self.characters[0], self.characters[1])

            elif opt == "q":
                break

            else:
                print("Invalid option, try again.")

        
    def show_characters(self):
        display_character_sheet(self.characters, HORIZONTRAL_SHEET_VIEW)

    def _setup(self):
        self._load_chars()

    def _save_characters(self, filepath: str = None):
        if filepath is None:
            filepath = CHARS_DATA_PATH

        arr = [char.to_dict() for char in self.characters]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(arr, f, ensure_ascii=False, indent=2)
        
    def _load_chars(self, filepath: str = None) -> list[Character]:
        if filepath is None:
            filepath = CHARS_DATA_PATH

        data = json.load(open(filepath, "r", encoding="utf-8"))
        # Se forem objetos gerados por to_dict(), talvez precise converter de volta.
        # Se forem objetos crus (mesmo formato de chars.json), basta usar Character(**data).
        self.characters = [Character(**char_data) for char_data in data]