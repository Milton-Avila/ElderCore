from rpg.models.character import Character

class Sorcerer(Character):
    BASE_HP = 8

    def __init__(self, **kwargs):
        super().__init__(**kwargs, base_hp=self.BASE_HP)
        