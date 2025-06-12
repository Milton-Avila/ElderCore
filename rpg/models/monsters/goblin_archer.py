import random

# Local
from rpg.models.entity import Entity

class Goblin(Entity):
    BASE_HP = 8

    def __init__(self):
        super().__init__(
            name="Goblin Rasteiro",
            title="O Espreitador",
            level=1,
            attributes={
                "dexterity": 14,
                "constitution": 8,
                "strength": 10
            },
            base_hp=self.BASE_HP
        )

    @property
    def base_dmg(self):
        return 3  # Arco Velho

    @property
    def prof_bonus(self):
        return self.get_attr_mod("dexterity")

    def choose_action(self):
        if random.random() < 0.2:
            return self.poison_arrow()
        return self.attack()