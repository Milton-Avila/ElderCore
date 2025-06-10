from rpg.packages import DEFAULT_ATTR_SCORE
from rpg.packages import ATTR_NAMES

class CombatStats:
    def __init__(self, entity, base_hp: int):
        self._attrs: Attributes = entity.attributes
        self._level: int = entity.level
        self._base_hp: int = base_hp

        self._update_stats()

    def _update_stats(self):
        self.hp_max = self._calc_hp_max()
        self.hp = self.hp_max
        self.damage_reduction = self._calc_damage_reduction()

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> None:
        self.hp = max(0, self.hp - max(0, amount))

    def heal(self, amount: int) -> None:
        self.hp = min(self.hp_max, self.hp + max(0, amount))

    def _calc_hp_max(self) -> int:
        const_mod = self._attrs.get_modifier('constitution')
        bonus_hp_level = self._base_hp // 2
        return self._base_hp + const_mod + (bonus_hp_level + const_mod) * (self._level - 1)

    def _calc_damage_reduction(self) -> int:
        return self._attrs.get_modifier('constitution')

    def to_dict(self) -> dict:
        return {
            "hp_max": self.hp_max,
            "hp": self.hp,
            "damage_reduction": self.damage_reduction
        }


class Attributes:
    def __init__(self, base: dict[str, int]):
        self._values: dict[str, int] = {
            attr: base.get(attr, DEFAULT_ATTR_SCORE)
            for attr in ATTR_NAMES
        }

    @property
    def values(self) -> dict[str, int]:
        return self._values.copy()

    @property
    def modifiers(self) -> dict[str, int]:
        return {
            attr: self._calc_mod(score)
            for attr, score in self._values.items()
        }

    def get_modifier(self, attr: str) -> int:
        if attr not in ATTR_NAMES:
            raise ValueError(f"Invalid attribute: {attr}")
        return self._calc_mod(self._values[attr])

    def to_dict(self) -> dict[str, int]:
        return self._values.copy()

    def _calc_mod(self, val: int) -> int:
        return (val - 10) // 2