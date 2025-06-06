import json

# Local
from rpg.packages import ATTR_NAMES, EQUIPMENT_SLOTS
from rpg.models.equipment import Equipment, EmptySlot
from rpg.models.attributes import Attributes, CombatStats

class Entity:
    def __init__(self, name: str, title: str, level: int, attributes: dict):

        self.name = name
        self.title = title
        self.level = level
        self.attributes = Attributes(attributes)
        
        attr = self.attributes.to_dict()
        self.combat_stats = CombatStats(level, attr)

    @property
    def alive(self):
        return self.combat_stats.is_alive()
    
    @property
    def hp_max(self):
        return self.combat_stats.hp_max
    
    @property
    def hp_current(self):
        return self.combat_stats.hp_current
    
    @property
    def ac(self):
        return self.combat_stats.ac
    
    def get_attr(self, attr: str) -> int:
        if attr not in ATTR_NAMES:
            raise ValueError(f"Invalid attribute: {attr}")
        return self.attributes.values[attr]
    
    def get_bonus_attr(self, attr: str) -> int:
        if attr not in ATTR_NAMES:
            raise ValueError(f"Invalid attribute: {attr}")
        return self.attributes.get_bonus_attrs().get(attr, 0)

    def take_damage(self, amount: int):
        self.combat_stats.take_damage(amount)

    def heal(self, amount: int):
        self.combat_stats.heal(amount)

    def spend_sp(self, amount: int):
        self.combat_stats.spend_sp(amount)

    def restore_sp(self, amount: int):
        self.combat_stats.restore_sp(amount)

class Character(Entity):
    def __init__(self, name: str, title: str, level: int, attributes: dict, equipment: list[dict] = []):
        
        super().__init__(name, title, level, attributes)
        self.equipment = self._load_equipment(equipment)
        
    @property
    def bio(self):
        return {
            'name': self.name,
            'level': self.level,
            'title': self.title,
            'combat_stats': self.combat_stats.to_dict()
        }
    
    @property
    def sp_max(self):
        return self.combat_stats.sp_max
    
    @property
    def sp_current(self):
        return self.combat_stats.sp_current
    
    @property
    def equipment_mod(self):
        modifiers = {}
        for item in self.equipment.values():
            for attr, val in item.get_modifiers().items():
                modifiers[attr] = modifiers.get(attr, 0) + val
        return modifiers
    
    @property
    def base_dmg(self) -> str:
        weapon = self.get_equipment('main_hand')
        if not weapon or isinstance(weapon, EmptySlot):
            weapon = self.get_equipment('off_hand')

        return weapon.get_base_dmg()

    @property
    def final_attrs(self):
        modifiers = self.equipment_mod
        return self.attributes.get_final_attrs(modifiers)

    @property
    def bonus_attrs(self):
        return self.attributes.get_bonus_attrs(self.equipment_mod)
    
    def get_equipment(self, slot: str):
        return self.equipment.get(slot, None)

    def equip(self, item_data: dict):
        slot = item_data.get('slot', None)

        if isinstance(self.equipment.get(slot), EmptySlot):
            self.equipment[slot] = Equipment(
                self.load_item(item_data)
            )
            return
        else:
            raise ValueError(f"Slot '{slot}' is already occupied by '{self.get_equipment(slot)}'.")
    
    @classmethod
    def _load_equipment(cls, equipment_data: list[dict]) -> dict[str, Equipment]:
        equipment = {}
        
        for item_data in equipment_data:
            equipment[item_data['slot']] = cls.load_item(item_data)
        
        # Fill empty slots with EmptySlot instances
        for slot in EQUIPMENT_SLOTS:
            if slot not in equipment:
                equipment[slot] = EmptySlot(slot)

        return equipment
    
    @classmethod
    def load_item(cls, item_data: dict):
        name = item_data['name']
        title = item_data.get('title', '')
        slot = item_data.get('slot', None)
        base_dmg = item_data.get('base_dmg', 0)
        dmg_type = item_data.get('dmg_type', 'bludgeoning')
        modifiers = item_data.get('modifiers', {})
        
        if slot not in EQUIPMENT_SLOTS:
            raise ValueError(f"Invalid equipment slot: {slot}")

        return Equipment(
            name=name,
            title=title,
            base_dmg=base_dmg,
            dmg_type=dmg_type,
            slot=slot,
            modifiers=modifiers
        )

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