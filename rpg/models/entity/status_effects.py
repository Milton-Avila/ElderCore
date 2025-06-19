from abc import ABC


class StatusEffect(ABC):
    message: str
    remaining_turns: int

    def __init__(self):
        pass

    def apply(self, entity):
        pass

    def on_turn_start(self, entity):
        pass

    def on_turn_end(self, entity):
        pass


# Specific
class DefenseStatus(StatusEffect):

    def __init__(self, dmg_reduction_per_turn, duration):
        self.dmg_reduction = dmg_reduction_per_turn
        self.remaining_turns = duration

    def apply(self, entity):
        self.message = f'{entity.name} está defendendo e ganha {entity.get_attr_mod("constitution")} shield!'
        self.remaining_turns -= 1


class BleedingEffect(StatusEffect):
    def __init__(self, damage_per_turn=1, duration=3):
        self.damage = damage_per_turn
        self.remaining_turns = duration

    def apply(self, entity):
        entity.take_damage(self.damage)
        print(f'{entity.name} sangra e perde {self.damage} HP!')
        self.remaining_turns -= 1


class PoisonedStatus(StatusEffect):
    def __init__(self, damage_per_turn=1, duration=3):
        self.damage = damage_per_turn
        self.remaining_turns = duration

    def apply(self, entity):
        entity.take_damage(self.damage)
        print(f'{entity.name} está envenenado e perde {self.damage} HP!')
        self.remaining_turns -= 1
