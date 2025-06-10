import random

# Local
from rpg.models.entity import Entity

class DamageSystem:
    @staticmethod
    def resolve_attack(attacker: Entity, defender: Entity):
        base = attacker.base_dmg
        variance = int(base * 0.15)
        raw = random.randint(base - variance, base + variance)
        reduced = DamageSystem.apply_reductions(raw, defender)
        defender.take_damage(reduced)
        print(f"{attacker.name} causa {reduced} de dano a {defender.name}!")

    @staticmethod
    def apply_reductions(damage: int, defender: Entity) -> int:
        mitigation = int(defender.damage_reduction * 0.5)
        return max(1, damage - mitigation)