from rpg.models.character import Character
from rpg.models.equipment import EmptySlot, Equipment

class Werebeast(Character):
    BASE_HP = 12

    def __init__(self, **kwargs):
        super().__init__(**kwargs, base_hp=self.BASE_HP)
        self.natural_weapon = Equipment(
            'Bestial Claws',
            '',
            'natural',
            '1d8',
            'slashing',
            'strength'
        )

    @property
    def main_weapon(self) -> Equipment:
        # prioriza main_hand, depois off_hand, depois natural
        for slot in ('main_hand', 'off_hand'):
            item = self.equipment.get(slot)
            if item and not isinstance(item, EmptySlot):
                return item
        return self.natural_weapon