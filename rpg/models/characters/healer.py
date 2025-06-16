from dataclasses import dataclass

# Local
from rpg.models.characters.character import Character

@dataclass
class Healer(Character):
    BASE_HP = 8

    def __init__(self, **kwargs):
        super().__init__(**kwargs)