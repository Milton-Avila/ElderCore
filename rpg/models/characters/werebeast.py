from dataclasses import dataclass

# Local
from rpg.models.characters.character import Character
from rpg.models.base.equipment import Equipment
from rpg.models.base.item import HandItem, EMPTY_SLOT

@dataclass
class Werebeast(Character):
    BASE_HP = 12

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.natural_weapon = HandItem(
            name='Bestial Claws',
            title='Life Ender',
            slot='Natural Weapon',
            base_dmg=5
        )

    @property
    def main_weapon(self) -> HandItem:
        # prioriza main_hand, depois off_hand, depois natural
        for slot in ('main_hand', 'off_hand'):
            item = self.equipment.get(slot)
            if item and item != EMPTY_SLOT:
                return item
        return self.natural_weapon