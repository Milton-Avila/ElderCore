import json

# Local
from src.packages.char_sheet import EQUIPMENT_SLOTS
from src.utils.sheet_view import display_character_sheet
from src.models.character import Character

class RPGSystem:
    def __init__(self):
        self.characters = []

    def setup(self):
        self._load_chars()
        
    def show_characters(self):
        display_character_sheet(self.characters)

    def _load_chars(self):
        with open('src/data/chars.json', 'r', encoding='utf-8') as file:
            characters_data = json.load(file, )

        characters = []

        for char_data in characters_data:
            character = Character(**char_data)
            characters.append(character)
        
        self.characters = characters