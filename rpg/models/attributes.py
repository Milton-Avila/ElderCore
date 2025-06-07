from rpg.packages import DEFAILT_AC, DEFAULT_ATTR_SCORE
from rpg.packages import ATTR_NAMES

class CombatStats:
    def __init__(self, level: int, attrs: dict[str, int], base_hp: int):
        self.update_stats(level, attrs, base_hp)

    def update_stats(self, level: int, attrs: dict[str, int], base_hp: int) -> None:
        self.hp_max = self._calc_hp_max(level, attrs, base_hp)
        self.hp_current = self.hp_max
        self.ac = self._calc_ac(attrs)
        
    def is_alive(self) -> bool:
        return self.hp_current > 0

    def take_damage(self, amount: int) -> None:
        if amount > 0:
            self.hp_current = max(0, self.hp_current - amount)

    def heal(self, amount: int) -> None:
        if amount > 0:
            self.hp_current = min(self.hp_max, self.hp_current + amount)

    def _calc_hp_max(self, level: int, attrs: dict[str, int], base_hp: int) -> int:
        const_mod = self._get_mod(attrs['constitution'])
        bonus_hp_level = base_hp // 2
        return base_hp + const_mod + (bonus_hp_level + const_mod) * (level -1)
        
    def _calc_ac(self, attrs: dict[str, int]) -> int:
        dex_mod = self._get_mod(attrs['dexterity'])
        con_mod = self._get_mod(attrs['constitution'])
        return DEFAILT_AC + dex_mod + con_mod
    
    def _get_mod(self, val: int) -> int:
        return (val -10) // 2

    def to_dict(self) -> dict:
        return {
            "hp_max": self.hp_max,
            "hp_current": self.hp_current,
            "ac": self.ac
        }

class Attributes:
    def __init__(self, base: dict):
        self.values: dict[str, int] = {attr: base.get(attr, DEFAULT_ATTR_SCORE) for attr in ATTR_NAMES}

    def get_attr_bonus(self) -> dict[str, int]:
        return {attr: (val -10) // 2 for attr, val in self.values.items()}

    def to_dict(self) -> dict[str, int]:
        return self.values.copy()