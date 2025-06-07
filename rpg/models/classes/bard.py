from rpg.models.character import Character

class Bard(Character):
    BASE_HP = 8

    def __init__(self, **kwargs):
        super().__init__(**kwargs, base_hp=self.BASE_HP)
        