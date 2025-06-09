
import random

class DamageSystem:
    @staticmethod
    def resolve_attack(attacker, defender):
        base = attacker.attack_power
        variance = base * 0.15
        raw = random.uniform(base - variance, base + variance)
        reduced = DamageSystem.apply_reductions(raw, defender)
        defender.hp -= int(reduced)
        print(f"{attacker.name} causa {int(reduced)} de dano a {defender.name}!")

    @staticmethod
    def apply_reductions(damage, defender):
        mitigation = defender.constitution * 0.5
        return max(1, damage - mitigation)