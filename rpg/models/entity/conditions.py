from dataclasses import dataclass, field

# Local
from rpg.models.entity.status_effects import StatusEffect


class Conditions:
    def __init__(self, status_effects:list ={}):
        self.status_effects = status_effects

    @property
    def stunned(self) -> bool:
        return 'stunned' in self.status_effects

    def add_status_effect(self, key:str, effect: StatusEffect):
        self.status_effects[key] = ...

    def cleanup_expired_effects(self):
        self.status_effects = {
            name: effect for name, effect in self.status_effects.items()
            if getattr(effect, 'remaining_turns', 1) > 0
        }

    def apply_status_effects(self, entity):
        ...

        # for name, eff in list(self.status_effects.items()):
        #     eff.apply(entity)
        #     if getattr(eff, "remaining_turns", 1) <= 0:
        #         del self.status_effects[name]