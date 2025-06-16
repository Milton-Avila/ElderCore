from dataclasses import dataclass, field
from rpg.models.base.item import HandItem, HeadItem, EMPTY_SLOT

class Equipment:
    def __init__(self, equip_data: list[dict]):
        self.slots = {
            item_data['slot']: self.__load_item(item_data)
            for item_data in equip_data
        }

    @property
    def main_hand(self) -> HandItem:
        return self.slots.get('main_hand', EMPTY_SLOT)

    @property
    def off_hand(self) -> HandItem:
        return self.slots.get('off_hand', EMPTY_SLOT)

    def get_equipment(self, slot:str) -> HandItem|HeadItem:
        return self.slots.get(slot, EMPTY_SLOT)

    def equip(self, item_data: dict):
        slot = item_data.get('slot')
        if self.slots.get(slot) == EMPTY_SLOT:
            self.slots[slot] = self.__load_item(item_data)
        else:
            raise ValueError(f"Slot '{slot}' is already occupied.")

    @staticmethod
    def __load_item(item_data: dict) -> HandItem|HeadItem:
        cls = HandItem if item_data.get('base_dmg', False) else HeadItem
        return cls(**item_data)