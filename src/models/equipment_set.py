from src.models.equipment import Equipment

class EquipmentSet:
    def __init__(self):
        self.head: Equipment = None
        self.left_hand: Equipment = None
        self.right_hand: Equipment = None

    def add_equipment(self, slot: str, item: Equipment):
        if slot in self.equipment:
            self.equipment[slot] = item
        else:
            raise ValueError(f"Invalid equipment slot: {slot}")

    def __repr__(self):
        return f"EquipmentSet(id={self.equipment_set_id}, name='{self.name}', description='{self.description}')"