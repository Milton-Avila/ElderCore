from rpg.models.action import Action
from rpg.packages import ATTR_NAMES
from rpg.models.attributes import Attributes, CombatStats
from rpg.models.status_effect import StatusEffect

class Entity:
    def __init__(self, name: str, title: str, level: int, attributes: dict, base_hp: int):
        self.name = name
        self.title = title
        self.level = level
        self._attributes = Attributes(attributes)
        self._combat_stats = CombatStats(self, base_hp)
        self._status_effects: dict[str, StatusEffect] = {}

    @property
    def base_dmg(self) -> int:
        ...  # This should be defined in subclasses

    @property
    def alive(self) -> bool:
        return self._combat_stats.is_alive()

    @property
    def hp_max(self) -> int:
        return self._combat_stats.hp_max

    @property
    def hp(self) -> int:
        return self._combat_stats.hp

    @property
    def attributes(self) -> Attributes:
        return self._attributes

    @property
    def initiative(self) -> int:
        return self.get_attr_mod("dexterity")

    @property
    def prof_bonus(self) -> int:
        raise NotImplementedError("Subclasses must implement prof_bonus")

    @property
    def damage_reduction(self) -> int:
        return self._combat_stats.damage_reduction
    
    @property
    def status_effects(self) -> list[StatusEffect]:
        return list(self._status_effects.values())
    
    @property
    def stunned(self) -> bool:
        return "stunned" in self._status_effects

    def get_attr(self, attr: str) -> int:
        if attr not in ATTR_NAMES:
            raise ValueError(f"Invalid attribute: {attr}")
        return self.attributes.values[attr]

    def get_attr_mod(self, attr: str) -> int:
        return self.attributes.get_modifier(attr)

    def take_damage(self, amount: int) -> None:
        self._combat_stats.take_damage(amount)

    def heal(self, amount: int) -> None:
        self._combat_stats.heal(amount)

    def apply_status_effects(self):
        for name, effect in list(self._status_effects.items()):
            effect.apply(self)
            if getattr(effect, 'remaining_turns', 1) <= 0:
                del self._status_effects[name]

    def add_status_effect(self, name: str, effect: StatusEffect):
        self._status_effects[name] = effect
    
    def cleanup_expired_effects(self):
        self._status_effects = {name: effect for name, effect in self._status_effects.items() if getattr(effect, 'remaining_turns', 1) > 0}

    def attack(self):
        return Action(
            self,
            "Attack",
            "attack",
            "Attacks the target, dealing damage based on attributes and equipment.",
            effect=lambda target: target.take_damage(self.base_dmg + self.prof_bonus)
        )

    def defend(self):
        return Action(
            self,
            "Defend",
            "defend",
            "Defends against the next attack, reducing damage taken."
        )