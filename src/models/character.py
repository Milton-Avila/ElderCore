import json

# Local
from src.packages import ATTR_NAMES, EQUIPMENT_SLOTS
from src.models.equipment import Equipment, EmptySlot
from src.models.attributes import Attributes, CombatStats

class Entity:
    def __init__(self, name: str, title: str, level: int, attributes: dict):
        
        self.name = name
        self.title = title
        self.level = level
        self.attributes = Attributes(attributes)
        
        attr = self.attributes.to_dict()
        self.combat_stats = CombatStats(level, attr)
    
    def get_attr(self, attr: str) -> int:
        if attr not in ATTR_NAMES:
            raise ValueError(f"Invalid attribute: {attr}")
        return self.attributes.values[attr]
    
    def get_bonus_attr(self, attr: str) -> int:
        if attr not in ATTR_NAMES:
            raise ValueError(f"Invalid attribute: {attr}")
        return self.attributes.get_bonus_attrs().get(attr, 0)

    def is_alive(self):
        return self.vitals.is_alive()

    def take_damage(self, amount: int):
        self.vitals.take_damage(amount)

    def heal(self, amount: int):
        self.vitals.heal(amount)

    def spend_sp(self, amount: int):
        self.vitals.spend_sp(amount)

    def restore_sp(self, amount: int):
        self.vitals.restore_sp(amount)

class Character(Entity):
    def __init__(self, name: str, title: str, level: int, attributes: dict, equipment: list[dict] = []):
        super().__init__(name, title, level, attributes)
        
        self.equipment = self._load_equipment(equipment)
        
    def get_bio(self):
        return {
            'name': self.name,
            'level': self.level,
            'title': self.title,
            'combat_stats': self.combat_stats.to_dict()
        }
    
    def get_equipment(self, slot: str):
        return self.equipment.get(slot, None)
    
    def get_equipment_mod(self):
        modifiers = {}
        for item in self.equipment.values():
            for attr, val in item.get_modifiers().items():
                modifiers[attr] = modifiers.get(attr, 0) + val
        return modifiers

    def get_final_attrs(self):
        modifiers = self.get_equipment_mod()
        return self.attributes.get_final_attrs(modifiers)

    def get_bonus_attrs(self):
        return self.attributes.get_bonus_attrs(self.get_equipment_mod())

    def equip(self, item_data: dict):
        name: str = item_data['name']
        title: str = item_data.get('title', '')
        modifiers = item_data.get('modifiers', {})
        slot = item_data.get('slot', None)

        if isinstance(self.equipment.get(slot), EmptySlot):
            self.equipment[slot] = Equipment(
                name=name,
                title=title,
                slot=slot,
                modifiers=modifiers
            )
            return
        else:
            raise ValueError(f"Slot '{slot}' is already occupied by '{self.get_equipment(slot)}'.")
    
    @staticmethod
    def _load_equipment(equipment_data: list[dict]) -> dict[str, Equipment]:
        equipment = {}
        for item_data in equipment_data:
            name = item_data['name']
            title = item_data.get('title', '')
            slot = item_data.get('slot', None)
            modifiers = item_data.get('modifiers', {})

            if slot not in EQUIPMENT_SLOTS:
                raise ValueError(f"Invalid equipment slot: {slot}")

            equipment[slot] = Equipment(
                name=name,
                title=title,
                slot=slot,
                modifiers=modifiers
            )
        
        # Fill empty slots with EmptySlot instances
        for slot in EQUIPMENT_SLOTS:
            if slot not in equipment:
                equipment[slot] = EmptySlot(slot)

        return equipment

    @classmethod
    def from_jsonfile(cls, path: str) -> list['Character']:
        data = json.load(open(path, 'r', encoding='utf-8'))
        return [cls(**char_data) for char_data in data]

    def to_dict(self) -> dict:
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
                {
                    'name': item.name,
                    'title': item.title,
                    'slot': item.slot,
                    'modifiers': item.get_modifiers()
                } if item.title else {
                    'name': item.name,
                    'slot': item.slot,
                    'modifiers': item.get_modifiers()
                }
                for slot, item in self.equipment.items()
                if not isinstance(item, EmptySlot)
            ]
        }