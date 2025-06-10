# Local
from rpg.packages import EQUIPMENT_SLOTS
from rpg.models.equipment import Equipment, EMPTY_SLOT
from rpg.models.entity import Entity
from rpg.models.action import Action

class Character(Entity):
    def __init__(self, name: str, title: str, level: int, attributes: dict, base_hp: int, equipment: list[dict] = []):
        super().__init__(name, title, level, attributes, base_hp)
        self.equipment = self._load_equipment(equipment)
        self.skills: list[Action] = []

    @property
    def bio(self) -> dict:
        return {
            'name': self.name,
            'level': self.level,
            'title': self.title,
            'combat_stats': self._combat_stats.to_dict()
        }
    
    @property
    def base_dmg(self) -> int:
        weapon = self.main_weapon
        if weapon == EMPTY_SLOT:
            return 1
        return weapon.base_dmg

    @property
    def main_weapon(self) -> Equipment:
        for slot in ('main_hand', 'off_hand'):
            item = self.equipment.get(slot)
            if item and item != EMPTY_SLOT:
                return item
        return EMPTY_SLOT

    @property
    def prof_bonus(self) -> int:
        weapon = self.get_equipment('main_hand')
        if weapon == EMPTY_SLOT:
            weapon = self.get_equipment('off_hand')
        return self.get_attr_mod(weapon.proficience_mod)
    
    def choose_action(self):
        print(f"{self.name}'s turn. Choose an action:")
        print('1. Attack')
        print('2. Defend')
        print('3. skills')
        print('4. Use Item')
        while True:
            match input('> '):
                case '1':
                    return self.attack()
                case '2':
                    return self.defend()
                case '3':
                    return self.use_skill()
                case '4':
                    return self.use_item()
                case _:
                    print('Invalid choice, try again.')
    
    def use_skill(self):
        ...  # This should be defined in subclasses

    def use_item(self):
        ...  # This should be defined in subclasses
            

    def get_equipment(self, slot: str) -> Equipment:
        return self.equipment.get(slot, EMPTY_SLOT)

    def equip(self, item_data: dict):
        slot = item_data.get('slot')
        if self.equipment.get(slot) == EMPTY_SLOT:
            self.equipment[slot] = self._load_item(item_data)
        else:
            raise ValueError(f"Slot '{slot}' is already occupied by '{self.get_equipment(slot)}'.")

    @classmethod
    def _load_equipment(cls, equipment_data: list[dict]) -> dict[str, Equipment]:
        equipment = {item['slot']: cls._load_item(item) for item in equipment_data}
        for slot in EQUIPMENT_SLOTS:
            equipment.setdefault(slot, EMPTY_SLOT)
        return equipment

    @classmethod
    def _load_item(cls, item_data: dict) -> Equipment:
        return Equipment(
            name=item_data['name'],
            title=item_data.get('title', ''),
            slot=item_data['slot'],
            base_dmg=item_data.get('base_dmg', 1),
            dmg_type=item_data.get('dmg_type', 'bludgeoning'),
            proficience_mod=item_data.get('proficience_mod', 'strength')
        )

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'title': self.title,
            'level': self.level,
            'attributes': {k: v for k, v in self.attributes.to_dict().items() if v != 8},
            'equipment': [item.asdict() for slot, item in self.equipment.items() if item != EMPTY_SLOT]
        }
