import json

# Local
from rpg.packages import EQUIPMENT_SLOTS
from rpg.models.equipment import Equipment, EmptySlot
from rpg.models.entity import Entity

class Character(Entity):
    def __init__(self, name: str, title: str, level: int, attributes: dict, base_hp: int, equipment: list[dict] = []):
        super().__init__(name, title, level, attributes, base_hp)
        self.equipment = self._load_equipment(equipment)
        
    @property
    def bio(self) -> dict[str, str | int]:
        return {
            'name': self.name,
            'level': self.level,
            'title': self.title,
            'combat_stats': self._combat_stats.to_dict()
        }
    
    @property
    def main_weapon(self) -> Equipment:
        for slot in ("main_hand", "off_hand"):
            item = self.equipment.get(slot)
            if item and not isinstance(item, EmptySlot):
                return item
        return item
    
    @property
    def prof_bonus(self) -> str:
        weapon = self.get_equipment('main_hand')
        if not weapon or isinstance(weapon, EmptySlot):
            weapon = self.get_equipment('off_hand')

        proficience_mod = weapon.proficience_mod
        return self.get_attr_bonus(proficience_mod)
    
    def get_equipment(self, slot: str) -> Equipment | EmptySlot:
        return self.equipment.get(slot, EmptySlot)

    def equip(self, item_data: dict):
        slot = item_data.get('slot', None)

        if isinstance(self.equipment.get(slot), EmptySlot):
            self.equipment[slot] = Equipment(
                self._load_item(item_data)
            )
            return
        else:
            raise ValueError(f"Slot '{slot}' is already occupied by '{self.get_equipment(slot)}'.")
    
    @classmethod
    def _load_equipment(cls, equipment_data: list[dict]) -> dict[str, Equipment]:
        equipment = {}
        
        for item_data in equipment_data:
            equipment[item_data['slot']] = cls._load_item(item_data)
        
        # Fill empty slots with EmptySlot instances
        for slot in EQUIPMENT_SLOTS:
            if slot not in equipment:
                equipment[slot] = EmptySlot(slot)

        return equipment
    
    @classmethod
    def _load_item(cls, item_data: dict) -> Equipment:
        name = item_data['name']
        title = item_data.get('title', '')
        slot = item_data.get('slot', None)
        base_dmg = item_data.get('base_dmg', 0)
        dmg_type = item_data.get('dmg_type', 'bludgeoning')
        proficience_mod = item_data.get('proficience_mod', 'strength')
        
        if slot not in EQUIPMENT_SLOTS:
            raise ValueError(f"Invalid equipment slot: {slot}")

        return Equipment(
            name,
            title,
            slot,
            base_dmg,
            dmg_type,
            proficience_mod
        )

    @classmethod
    def from_jsonfile(cls, path: str) -> list['Character']:
        data = json.load(open(path, 'r', encoding='utf-8'))
        return [cls(**char_data) for char_data in data]

    def to_dict(self) -> dict[str, str | int | dict | list[dict]]:
        return {
            'name': self.name,
            'title': self.title,
            'level': self.level,
            'attributes': {
                attr: val
                for attr, val in self.attributes.to_dict().items()
                if val != 8
            },
            'equipment': [
                item.asdict()
                for slot, item in self.equipment.items()
                if not isinstance(item, EmptySlot)
            ]
        }