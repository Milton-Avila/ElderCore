from rpg.combat.turn_processor import TurnProcessor

class CombatLoop:
    def __init__(self, allies, enemies):
        self.allies = allies
        self.enemies = enemies
        self.turn_order = self._define_turn_order()

    def start_combat(self):
        round_count = 1
        while not self._check_end_condition():
            for actor in self.turn_order:
                if actor.hp <= 0:
                    continue
                TurnProcessor.process_turn(actor, self.allies, self.enemies)
            round_count += 1

    def _check_end_condition(self):
        return all(a.hp <= 0 for a in self.allies) or all(e.hp <= 0 for e in self.enemies)
