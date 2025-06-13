import random

# Local
from rpg.combat.aggro import AggroSystem
from rpg.models.action import Action
from rpg.models.entity import Entity
from rpg.models.status_effect import PoisonedStatus

class Goblin(Entity):
    BASE_HP = 8

    def __init__(self):
        super().__init__(
            name='Goblin Rasteiro',
            title='O Espreitador',
            level=1,
            attributes={\
                'dexterity': 14,
                'constitution': 8,
                'strength': 10
            },
            base_hp=self.BASE_HP
        )

    @property
    def base_dmg(self):
        return 3  # Arco Velho

    @property
    def prof_bonus(self):
        return self.get_attr_mod('dexterity')

    def choose_action(self, allies: list[Entity], enemies: list[Entity], aggro_system: AggroSystem):
        target = aggro_system.get_primary_target(enemies)
        
        if random.random() < 0.2:
            return self.poison_arrow(target)
        return self.attack(target)
    
    def poison_arrow(self, target: Entity):
        return Action(
                actor=self,
                name='Poison Arrow',
                kind='skill',
                description='Shoots a poisoned arrow',
                effect=lambda: (
                target.take_damage(self.base_dmg // 2 + self.prof_bonus),
                target.add_status_effect('poisoned', PoisonedStatus(turns=3))
            )
        )