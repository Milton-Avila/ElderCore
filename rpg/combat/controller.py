from rpg.combat.loop import CombatLoop

class CombatController:
    @classmethod
    def duel(cls, allies: list, enemies: list) -> None:
        loop = CombatLoop(allies, enemies)
        loop.start_combat()