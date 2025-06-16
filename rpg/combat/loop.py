from rpg.utils.auxiliar_func import clear
from rpg.models.characters.character import Character
from rpg.models.base.entity import Entity
from rpg.combat.status import StatusSystem
from rpg.combat.actions import ActionSystem

class CombatLoop:
    def __init__(self, allies: list[Character], enemies: list[Entity]):
        self.allies = allies
        self.enemies = enemies
        self.turn_order = self._define_turn_order()

    def start_combat(self):
        round_count = 1
        while True:
            for actor in self.turn_order:
                if actor.hp <= 0:
                    continue
                print(f"=== Round {round_count} ===")
                TurnProcessor.process_turn(actor, self.allies, self.enemies)
                if self._check_end_condition():
                    break
            round_count += 1

    def _check_end_condition(self):
        return all(a.hp <= 0 for a in self.allies) or all(e.hp <= 0 for e in self.enemies)

    def _define_turn_order(self) -> list[Entity]:
        return sorted(self.allies + self.enemies, key=lambda x: x.initiative, reverse=True)


class TurnProcessor:
    @staticmethod
    def process_turn(actor: Entity, allies: list[Character], enemies: list[Entity]):
        StatusSystem.apply_effects(actor)
        if actor.stunned:
            return
        action = actor.choose_action()
        ActionSystem.resolve(action, actor, allies, enemies)