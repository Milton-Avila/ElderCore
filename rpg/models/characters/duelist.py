# Local
from rpg.models.characters.character import Character

class Duelist(Character):
    BASE_HP: int = 10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)