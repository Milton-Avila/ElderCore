from dataclasses import dataclass


@dataclass(frozen=True)
class Equipment:
    name: str
    title: str
    _slot: str
    _base_dmg: str
    _dmg_type: str
    _proficience_mod: str
    
    @property
    def slot(self) -> str:
        return self._slot

    @property
    def base_dmg(self) -> str:
        return self._base_dmg
    
    @property
    def dmg_type(self) -> str:
        return self._dmg_type
    
    @property
    def proficience_mod(self) -> str:
        return self._proficience_mod
    
    def asdict(self) -> dict:
        item = {
            'name': self.name,
        }

        if self.title:
            item['title'] = self.title

        item['slot'] = self.slot

        if self.slot != 'head':
            item['base_dmg'] = self.base_dmg
            item['proficience_mod'] = self.proficience_mod
            item['dmg_type'] = self.dmg_type

        return item

    def __repr__(self):
        return f'{self.name}{f' ({self.title})' if self.title else ''}'

@dataclass(frozen=True)
class EmptySlot(Equipment):
    def __init__(self, slot: str):
        base_dmg = '1d2' if slot != 'head' else ''
        dmg_type = 'bludgeoning' if slot != 'head' else ''

        super().__init__(
            'Nothing',
            '',
            slot,
            base_dmg,
            dmg_type,
            "strength",
        )

    def __repr__(self):
        return 'Nothing'