from rpg.combat.damage import DamageSystem
from rpg.models.entity import Entity
from rpg.models.action import Action
from rpg.models.character import Character

class ActionSystem:
    @staticmethod
    def resolve(action: Action, actor: Entity, allies: list[Character], enemies: list[Entity]):
        if action.type == "attack":
            target = ActionSystem.choose_target(enemies)
            action.effect(target)
            DamageSystem.resolve_attack(actor, target)
        elif action.type == "defend":
            actor.defend()
        elif action.type == "ability":
            action.perform(actor, allies, enemies)
        elif action.type == "item":
            action.use_item(actor)

    @staticmethod
    def choose_target(possible_targets: list[Entity]):
        print("Choose a target:")
        for i, entity in enumerate(possible_targets):
            print(f"{i + 1}. {entity.name} (HP: {entity.hp})")
        while True:
            try:
                index = int(input("> ")) - 1
                return possible_targets[index]
            except (ValueError, IndexError):
                print("Invalid choice.")