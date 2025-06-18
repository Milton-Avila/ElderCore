import enum
from typing import List
from rpg.combat.actions import ActionSystem
from rpg.combat.aggro import AggroSystem
from rpg.combat.loop import CombatLoop

class CombatController:
    @classmethod
    def battle(cls, allies: list, enemies: list) -> None:
        session = CombatSession(allies, enemies)
        session.start()

from abc import ABC, abstractmethod
from rpg.models.entity.entity import Entity
from rpg.models.entity.action import Action

# === combat/engine.py ===
class Phase(ABC):
    @abstractmethod
    def execute(self, session: 'CombatSession', actor: Entity):
        ...

class StatusPhase(Phase):
    def execute(self, session: 'CombatSession', actor: Entity):
        StatusEffect.apply_effects(actor)

    def apply(self, entity):
        entity.take_damage(self.damage)
        print(f'{entity.name} está envenenado e perde {self.damage} HP!')
        self.remaining_turns -= 1


class DecisionPhase(Phase):
    def execute(self, session: 'CombatSession', actor: Entity):
        # pass context to choose_action
        actor.current_action = actor.choose_action(
            allies=session.get_allies(actor),
            enemies=session.get_enemies(actor),
            aggro_system=session.aggro
        )

class ResolutionPhase(Phase):
    def execute(self, session: 'CombatSession', actor: Entity):
        action: Action = actor.current_action
        session.action_system.resolve(
            action, actor,
            session.get_allies(actor),
            session.get_enemies(actor)
        )
        # update aggro after resolution if needed
        session.aggro.update_threat(actor, action.target, action.threat_value)

enums = ['STATUS', 'DECISION', 'RESOLUTION', 'END']

class Phases(enum.Enum):
    STATUS = 1
    DECISION = 2
    RESOLUTION = 3
    END = 4

class CombatSession:
    def __init__(self, allies: List[Entity], enemies: List[Entity]):
        self.allies = allies
        self.enemies = enemies
        self.combatants = allies + enemies
        self.turn_order = sorted(
            self.combatants,
            key=lambda c: c.initiative,
            reverse=True
        )
        self.aggro = AggroSystem()
        self.phases: List[Phase] = [StatusPhase(), DecisionPhase(), ResolutionPhase()]
        self.action_system = ActionSystem

    def get_allies(self, actor: Entity) -> List[Entity]:
        return self.allies if actor in self.allies else self.enemies

    def get_enemies(self, actor: Entity) -> List[Entity]:
        return self.enemies if actor in self.allies else self.allies

    def start(self):
        round_ = 1
        while self._ongoing():
            for actor in self.turn_order:
                if not actor.alive:
                    continue
                for phase in self.phases:
                    phase.execute(self, actor)
                    if not actor.alive:
                        break
            round_ += 1

    def _ongoing(self) -> bool:
        return any(a.alive for a in self.allies) and any(e.alive for e in self.enemies)
