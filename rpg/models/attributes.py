from rpg.packages import ATTR_NAMES

class Attributes:
    DEFAULT_SCORE = 8

    def __init__(self, base: dict):
        self.values = {attr: base.get(attr, self.DEFAULT_SCORE) for attr in ATTR_NAMES}

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

    def to_dict(self):
        return self.values.copy()

class CombatStats:
    def __init__(self, level: int, attr: dict[str, int]):
        self.update_stats(level, attr)

    def update_stats(self, level: int, attr: dict[str, int]):

        self.hp_max = self._calc_hp_max(level, attr)
        self.hp_current = self.hp_max

        self.ac = self._calc_ac(attr)
        
    def is_alive(self) -> bool:
        return self.hp_current > 0

    def take_damage(self, amount: int) -> None:
        if amount > 0:
            self.hp_current = max(0, self.hp_current - amount)

    def heal(self, amount: int) -> None:
        if amount > 0:
            self.hp_current = min(self.hp_max, self.hp_current + amount)

    def spend_sp(self, amount: int):
        self.sp_current = max(0, self.sp_current - amount)

    def restore_sp(self, amount: int):
        self.sp_current = min(self.sp_max, self.sp_current + amount)
    
    def _calc_ac(self, attr: dict[str, int]) -> int:
        dex_mod = attr['dexterity']
        return 10 + dex_mod

    def to_dict(self) -> dict:
        return {
            "hp_current": self.hp_current,
            "hp_max": self.hp_max,
            "sp_current": self.sp_current,
            "sp_max": self.sp_max,
            "ac": self.ac
        }