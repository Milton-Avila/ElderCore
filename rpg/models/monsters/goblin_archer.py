import random

# Local
from rpg.combat.aggro import AggroSystem
from rpg.models.entity.action import Action
from rpg.models.entity.entity import Entity
from rpg.models.entity.conditions import PoisonedStatus

class Goblin(Entity):
    BASE_HP = 8
    
    name='Goblin Rasteiro'
    title='O Espreitador'
    _level=1
    _attrs_data={
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