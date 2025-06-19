from dataclasses import dataclass
from random import randint


@dataclass(frozen=True, kw_only=True)
class Item:
    name: str
    title: str

    def __str__(self):
        return f"{self.name}{f' ({self.title})' if self.title else ''}"


@dataclass(frozen=True, kw_only=True)
class HandItem(Item):
    base_dmg: int
    
    @property
    def damage_min_max(self) -> tuple[int, int]:
        variance = max(int(self.base_dmg * 0.2), 1)
        return self.base_dmg - variance, self.base_dmg + variance

    def damage_hit(self) -> int:
        '''Return randomized damage with ±20% variance'''
        variance = max(int(self.base_dmg * 0.2), 1)
        return randint(self.base_dmg - variance, self.base_dmg + variance)


@dataclass(frozen=True, kw_only=True)
class HeadItem(Item):
    pass


# Singleton vazio
EMPTY_SLOT = Item(name='Nothing', title='')
