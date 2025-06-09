from rpg.packages import ATTR_NAMES
from rpg.utils.dice_system import dice
from rpg.models.attributes import Attributes, CombatStats
from rpg.models.status_effect import StatusEffect

class Entity:
    def __init__(self, name: str, title: str, level: int, attributes: dict, base_hp: int = 10):
        self.name = name
        self.title = title
        self.level = level
        self._attributes = Attributes(attributes)
        self.stats = CombatStats(level, self._attributes.to_dict(), base_hp)
        self._status_effects: dict[str, StatusEffect] = {}

    @property
    def alive(self) -> bool:
        return self.stats.is_alive()

    @property
    def hp_max(self) -> int:
        return self.stats.hp_max

    @property
    def hp_current(self) -> int:
        return self.stats.hp_current

    @property
    def attributes(self) -> Attributes:
        return self._attributes

    def get_attr(self, attr: str) -> int:
        if attr not in ATTR_NAMES:
            raise ValueError(f"Invalid attribute: {attr}")
        return self.attributes.values[attr]

    def get_attr_bonus(self, attr: str) -> int:
        if attr not in ATTR_NAMES:
            raise ValueError(f"Invalid attribute: {attr}")
        return self.attributes.get_attr_bonus().get(attr, 0)

    def take_damage(self, amount: int) -> None:
        self.stats.take_damage(amount)

    def heal(self, amount: int) -> None:
        self.stats.heal(amount)

    def roll_initiative(self) -> int:
        return dice.roll(f'1d20+{self.get_attr_bonus("dexterity")}')['result']

    def roll_attack(self) -> tuple[int, int]:
        roll = dice.roll(f'1d20+{self.prof_bonus}', possible_crit=True)
        return roll['result'], roll['crit']

    def apply_status_effects(self):
        for name, effect in list(self._status_effects.items()):
            effect.apply(self)
            if getattr(effect, 'remaining_turns', 1) <= 0:
                del self._status_effects[name]

    def add_status_effect(self, name: str, effect: StatusEffect):
        self._status_effects[name] = effect

    def defend(self):
        self.add_status_effect("defending", StatusEffect())

    @property
    def prof_bonus(self) -> int:
        raise NotImplementedError("Subclasses must implement prof_bonus")
