from src.packages.char_sheet import ATTR_NAMES

class Character:
    def __init__(self, name: str, title: str, attributes: dict, equipment: list[dict] = []):
        self.name = name
        self.title = title
        self.attributes = Attributes(attributes)
        self.equipment = {}  # slot -> Equipment

        for item_data in equipment:
            self.equip(item_data)

    def equip(self, item_data: dict):
        item = Equipment(
            name=item_data["name"],
            title=item_data["title"],
            slot=item_data["slot"],
            modifiers=item_data.get("modifiers", {})
        )
        self.equipment[item.slot] = item

    def get_equipment(self, slot: str):
        return self.equipment.get(slot, None)
    
    def get_equipment_attr_bonus(self):
        modifiers = {}
        for item in self.equipment.values():
            for attr, val in item.modifiers.items():
                modifiers[attr] = modifiers.get(attr, 0) + val
        return modifiers

    def get_final_attr(self):
        modifiers = {}
        for item in self.equipment.values():
            for attr, val in item.modifiers.items():
                modifiers[attr] = modifiers.get(attr, 0) + val
        return self.attributes.get_final_attr(modifiers)

    def get_bonus_attr(self):
        return self.attributes.get_bonus_attr()


class Equipment:
    def __init__(self, name: str, title: str, slot: str, modifiers: dict[str, int]):
        self.name = name
        self.title = title
        self.slot = slot  # e.g., 'main_hand', 'head'
        self.modifiers = modifiers or {}  # dict[str, int]

    def __repr__(self):
        return f"{self.name} ({self.title})"


class Attributes:
    DEFAULT_SCORE = 8

    def __init__(self, base: dict):
        self.values = {attr: base.get(attr, self.DEFAULT_SCORE) for attr in ATTR_NAMES}

    def to_dict(self):
        return self.values.copy()

    def get_final_attr(self, modifiers: dict[str, int]):
        return {
            attr: self.values.get(attr, 0) + modifiers.get(attr, 0)
            for attr in ATTR_NAMES
        }

    def get_bonus_attr(self):
        return {
            attr: (v - 10) // 2 if v > 10 else 0
            for attr, v in self.values.items()
        }