from rpg.combat.aggro import AggroSystem
from rpg.combat.damage import DamageSystem
from rpg.models.base.entity import Entity
from rpg.models.base.action import Action
from rpg.models.characters.character import Character

class ActionSystem:
    @staticmethod
    def resolve(action: Action, actor: Entity, allies: list[Character], enemies: list[Entity]):
        if action.type == "attack":
            if actor in allies:
                target = ActionSystem.choose_target(enemies)
            elif actor in enemies:
                target = AggroSystem.get_primary_target(allies)
            DamageSystem.resolve_attack(actor, target)
            if action.effect:
                action.effect(target)
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