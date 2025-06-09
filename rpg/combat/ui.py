class CombatUI:
    @staticmethod
    def show_status(combatants):
        for c in combatants:
            print(f"{c.name}: {c.hp} HP")

    @staticmethod
    def show_turn_summary(actor, action):
        print(f"{actor.name} realizou: {action}")

    @staticmethod
    def show_action_result(result):
        print(result)