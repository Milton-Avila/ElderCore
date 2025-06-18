from dataclasses import dataclass

# Local
from rpg.models.characters.character import Character
from rpg.models.entity.equipment import Equipment
from rpg.models.entity.item import HandItem, EMPTY_SLOT

@dataclass
class Werebeast(Character):
    BASE_HP = 12

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.natural_weapon = HandItem(
            name='Bestial Claws',
            title='Life Ender',
            base_dmg=4
        )

    @property
    def main_weapon(self) -> HandItem:
        if self.equipment.main_weapon == EMPTY_SLOT:
            return self.natural_weapon
        return self.natural_weapon