# turn_processor.py
from rpg.combat.status import StatusSystem
from rpg.combat.actions import ActionSystem
from rpg.models.entity import Entity
from rpg.models.character import Character

class TurnProcessor:
    @staticmethod
    def process_turn(actor: Entity, allies: list[Character], enemies: list[Entity]):
        StatusSystem.apply_effects(actor)
        if actor.stunned:
            return
        action = actor.choose_action()
        ActionSystem.resolve(action, actor, allies, enemies)