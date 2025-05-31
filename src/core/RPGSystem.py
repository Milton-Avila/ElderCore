import json

# Local
from src.models.character import Character
from src.models.equipment import Equipment, EquipmentSet

class RPGSystem:
    def __init__(self):
        self.characters = []
        self.equipments = []

    def setup(self):
        self._load_chars()
        self._load_equipments()

    def show_characters(self):
        for char in self.characters:
            char.display()

    def _load_chars(self):
        with open('src/data/chars.json', 'r', encoding='utf-8') as file:
            characters_data = json.load(file, )

        characters = []

        for char_data in characters_data:
            character = Character(**char_data)
            characters.append(character)
        
        self.characters = characters

    def _load_equipments(self):
        ...