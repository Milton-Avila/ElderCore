import random

# Local
from rpg.combat.aggro import AggroSystem
from rpg.models.base.action import Action
from rpg.models.base.entity import Entity
from rpg.models.base.conditions import PoisonedStatus

class Goblin(Entity):
    BASE_HP = 8
    
    name='Goblin Rasteiro'
    title='O Espreitador'
    level=1
    attrs_data={
        'dexterity':14,
        'constitution':8,
        'strength':10
    }
    

    @property
    def base_dmg(self):
        return 3  # Arco Velho

    @property
    def prof_bonus(self):
        return self.get_attr_mod('dexterity')