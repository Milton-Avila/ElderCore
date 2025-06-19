# rpg/models/action.py
from dataclasses import dataclass
from typing import Callable, Optional

@dataclass(frozen=True)
class Action:
    actor: object                    # quem realiza
    name: str
    kind: str                        # 'attack', 'skill', 'defend', 'item'
    description: str
    target: Optional[object] = None  # será preenchido na fase de decisão
    effect: Optional[Callable] = None
    threat_value: int = 0            # quantos pontos de aggro gera

    def perform(self):
        '''Executa o efeito da ação.'''
        if self.effect:
            self.effect()
