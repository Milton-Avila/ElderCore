from src.models.attributes import Attributes
from src.models.equipment_set import EquipmentSet

class Character:
    def __init__(self, name: str, description: str, attributes: dict):
        self.name = name
        self.description = description
        self.attributes = Attributes(**attributes)
        self.equipment = EquipmentSet()

    def __repr__(self):
        return f'Character(name={self.name}, description={self.description})'

    def __str__(self):
        return f'{self.name}: {self.description}'