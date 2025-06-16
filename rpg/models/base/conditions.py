from dataclasses import dataclass, field

# Local
from rpg.models.base.status_effects import StatusEffect


@dataclass(init=False, kw_only=True)
class Conditions:
    status_effects: dict = field(default_factory=dict)

    @property
    def stunned(self) -> bool:
        return 'stunned' in self.status_effects

    def add_status_effect(self, key: str, effect: StatusEffect):
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