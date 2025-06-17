from rpg.utils.auxiliar_func import clear
from rpg.models.characters.character import Character
from rpg.models.base.entity import Entity
from rpg.combat.actions import ActionSystem
from rpg.models.base.status_effects import StatusEffect


class CombatLoop:
    def battle(self, allies: list[Character], enemies: list[Entity]):
        self.allies = allies
        self.enemies = enemies
        self.turn_order = self._define_turn_order()
        
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
    @classmethod
    def process_turn(cls, actor: Entity, allies: list[Character], enemies: list[Entity]):
        cls.apply_effects(actor)
        if actor.stunned:
            return
        action = actor.choose_action()
        ActionSystem.resolve(action, actor, allies, enemies)

    @staticmethod
    def apply_effects(entity: Entity):
        for condition in entity.conditions_list:
            condition.apply()
        entity.conditions.cleanup_expired_effects()