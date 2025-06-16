from dataclasses import dataclass, field
from typing import Dict
from rpg.models.base.entity import Entity

@dataclass
class Enemy(Entity):
    behavior: str = "aggressive"  # pode ser um enum futuramente
    tags: list[str] = field(default_factory=list)

    @property
    def base_dmg(self) -> int:
        # Exemplo simples, poderia variar por behavior
        return 1 + self.level // 2

    @property
    def prof_bonus(self) -> int:
        # Inimigos genéricos têm bônus fixo por nível
        return max(1, self.level // 2)

    def choose_action(self, allies, enemies, aggro):
        # Aqui é onde o "AI rudimentar" entra
        # Por agora, só ataca o inimigo com menos HP
        target = max(enemies, key=lambda e: e.hp_max)
        return self.attack(target)