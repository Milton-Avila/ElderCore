from abc import ABC, abstractmethod
# Local
from rpg.models.base.character_sheet import CharacterSheet
from rpg.models.base.conditions import Conditions
from rpg.models.base.status_effects import StatusEffect


class Entity(ABC):
    BASE_HP: int

    name: str
    title: str
    level: int
    attrs_data: dict[str, int]

    def __init__(self):
        self.char_sheet = CharacterSheet(self.level, self.attrs_data, self.BASE_HP)
        self.conditions = Conditions()

    def describe(self) -> str:
        return f'{self.name}, {self.title} - Level {self.level} - HP: {self.hp}/{self.hp_max}'

    # 💀 Conditions
    @property
    def conditions_list(self) -> list[StatusEffect]:
        print(self.conditions.status_effects.items())
        return self.conditions.status_effects.items()

    @property
    def alive(self) -> bool:
        return self.char_sheet.alive

    @property
    def stunned(self) -> bool:
        return self.conditions.stunned

    # 📈 Combat Stats
    @property
    def hp(self) -> int:
        return self.char_sheet.hp
    
    @property
    def hp_max(self) -> int:
        return self.char_sheet.hp_max

    # 🎲 Atributos
    @property
    def initiative(self) -> int:
        return self.get_attr_mod("dexterity")

    def get_attr_mod(self, attr: str) -> int:
        return self.char_sheet.attrs.get_modifier(attr)

    # 💥 Actions
    def take_damage(self, amt:int):
        self.char_sheet.take_damage(amt)

    def heal(self, amt:int):
        self.char_sheet.heal(amt)