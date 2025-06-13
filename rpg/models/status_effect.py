class StatusEffect:
    def apply(self, entity):
        pass

    def on_turn_start(self, entity):
        pass

    def on_turn_end(self, entity):
        pass

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
