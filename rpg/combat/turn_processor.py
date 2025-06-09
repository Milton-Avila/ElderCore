# turn_processor.py
from rpg.combat.status import StatusSystem
from rpg.combat.actions import ActionSystem

class TurnProcessor:
    @staticmethod
    def process_turn(actor, allies, enemies):
        StatusSystem.apply_passive_effects(actor)
        if actor.is_stunned():
            return
        action = actor.choose_action()
        ActionSystem.resolve(action, actor, allies, enemies)
