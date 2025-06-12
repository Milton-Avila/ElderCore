from rpg.models.entity import Entity

class Goblin(Entity):
    BASE_HP = 10

    def __init__(self):
        super().__init__(
            name="Goblin Rasteiro",
            title="O Espreitador",
            level=1,
            attributes={
                "dexterity": 13,
                "constitution": 10,
                "strength": 10
            },
            base_hp=self.BASE_HP
        )

    @property
    def base_dmg(self):
        return 3  # Adaga enferrujada

    @property
    def prof_bonus(self):
        return self.get_attr_mod("dexterity")

    def choose_action(self):
        return self.attack()
