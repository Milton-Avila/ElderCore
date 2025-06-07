from rpg.models.character import Character

class Duelist(Character):
    BASE_HP = 10

    def __init__(self, **kwargs):
        super().__init__(**kwargs, base_hp=self.BASE_HP)
        