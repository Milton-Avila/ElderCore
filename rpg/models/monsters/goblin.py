from rpg.combat.aggro import AggroSystem
from rpg.models.monsters.enemy import Enemy

class Goblin(Enemy):
    BASE_HP = 10

    name='Goblin Rasteiro'
    title='O Espreitador'
    _level=1
    _attrs_data={
        'dexterity':13,
        'constitution':10,
        'strength':10
    }

    @property
    def base_dmg(self):
        return 3  # Adaga enferrujada

    @property
    def prof_bonus(self):
        return self.get_attr_mod('dexterity')