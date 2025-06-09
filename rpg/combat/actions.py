from rpg.combat.damage import DamageSystem

class ActionSystem:
    @staticmethod
    def resolve(action, actor, allies, enemies):
        if action.type == "attack":
            target = action.target
            DamageSystem.resolve_attack(actor, target)
        elif action.type == "defend":
            actor.defend()
        elif action.type == "ability":
            action.ability.activate(actor, allies, enemies)
        elif action.type == "item":
            action.item.use(actor)