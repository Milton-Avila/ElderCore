from dataclasses import dataclass, field

# Local
DEFAULT_ATTR_SCORE = 8
ATTR_NAMES = [
    'strength',
    'dexterity',
    'constitution',
    'intelligence',
    'wisdom',
    'charisma'
]


class CharacterSheet:
    def __init__(self, level: int, attrs_data: dict[str, int], base_hp: int):
        self._level = level
        self.attrs = Attributes(attrs_data)
        self.base_hp = base_hp

        self.hp = self.base_hp*2
        self.refresh()

    @property
    def alive(self) -> bool:
        return self.hp > 0

    def refresh(self):
        self.hp_max = self._calc_hp_max()
        self.hp = min(self.hp, self.hp_max)
        self.damage_reduction = self._calc_damage_reduction()

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - max(0, amount))

    def heal(self, amount: int) -> None:
        self.hp = min(self.hp_max, self.hp + max(0, amount))

    def _calc_hp_max(self) -> int:
        const_mod = self.attrs.get_modifier('constitution')
        bonus_hp_level = self.base_hp // 2
        return self.base_hp + const_mod + (bonus_hp_level + const_mod) * (self._level - 1)

    def _calc_damage_reduction(self) -> int:
        return self.attrs.get_modifier('constitution')

    def to_dict(self) -> dict:
        return {
            'hp_max': self.hp_max,
            'hp': self.hp,
            'level': self._level,
            'attrs': self.attrs.to_dict(),
            'damage_reduction': self.damage_reduction
        }


class Attributes:
    def __init__(self, attrs_data: dict[str, int]):
        self.refresh(attrs_data)

    def refresh(self, attrs_data: dict[str, int]):
        self._values = {
            attr: attrs_data.get(attr, DEFAULT_ATTR_SCORE)
            for attr in ATTR_NAMES
        }

    @property
    def values(self) -> dict[str, int]:
        return self._values.copy()

    @property
    def modifiers(self) -> dict[str, int]:
        return {
            attr: (self._values[score] - 10) // 2
            for attr, score in self._values.items()
        }

    def get_modifier(self, attr: str) -> int:
        if attr not in ATTR_NAMES:
            raise ValueError(f'Invalid attribute: {attr}')
        return (self._values[attr] - 10) // 2

    def to_dict(self) -> dict[str, int]:
        return self._values.copy()