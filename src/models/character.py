import json

# Local
from src.packages import ATTR_NAMES, EQUIPMENT_SLOTS
from src.models.equipment import Equipment, EmptySlot

class Entity:
    def __init__(self, name: str, title: str, level: int, attributes: dict):
        self.name = name
        self.title = title
        self.level = level
        self.attributes = Attributes(attributes)

        self.hp_max = self._calc_hp_max()
        self.hp_current = self.hp_max

    def take_damage(self, amount: int):
        self.hp_current = max(0, self.hp_current - amount)

    def heal(self, amount: int):
        self.hp_current = min(self.hp_max, self.hp_current + amount)
    
    def get_attr(self, attr: str):
        return self.attributes.values[attr]
    
    def get_bonus_attr(self, attr: str):
        return self.attributes.get_bonus_attrs().get(attr, 0)

    def _calc_hp_max(self) -> tuple[int, int]:
        const_mod = self.get_bonus_attr('constitution')
        return 8 + const_mod + (5 + const_mod) * (self.level -1)

class Character(Entity):
    def __init__(self, name: str, title: str, level: int, attributes: dict, equipment: list[dict] = []):
        super().__init__(name, title, level, attributes)

        self.equipment = self._load_equipment(equipment)
        
    def get_bio(self):
        return {
            'name': self.name,
            'level': self.level,
            'title': self.title,
            'hp_max': self.hp_max
        }

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
    
    def get_equipment(self, slot: str):
        return self.equipment.get(slot, None)
    
    def get_equipment_attr_mod(self):
        modifiers = {}
        for item in self.equipment.values():
            for attr, val in item.get_modifiers().items():
                modifiers[attr] = modifiers.get(attr, 0) + val
        return modifiers

    def get_final_attrs(self):
        modifiers = self.get_equipment_attr_mod()
        return self.attributes.get_final_attrs(modifiers)

    def get_bonus_attrs(self):
        return self.attributes.get_bonus_attrs(self.get_equipment_attr_mod())
    
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

class Attributes:
    DEFAULT_SCORE = 8

    def __init__(self, base: dict):
        self.values = {attr: base.get(attr, self.DEFAULT_SCORE) for attr in ATTR_NAMES}

    def to_dict(self):
        return self.values.copy()

    def get_final_attrs(self, modifiers: dict[str, int]):
        return {
            attr: self.values.get(attr, 0) + modifiers.get(attr, 0)
            for attr in ATTR_NAMES
        }

    def get_bonus_attrs(self, equipment_modifiers: dict[str, int] = {}):
        base_items = self.values.items()
        if equipment_modifiers:
            base_items = [
                (attr, value + equipment_modifiers.get(attr, 0))
                for attr, value in base_items
            ]

        return {
            attr: (val - 10)//2
            for attr, val in base_items
        }
