class Equipment:
    def __init__(self, name: str, title: str, slot: str, base_dmg: str, dmg_type: str, modifiers: dict[str, int] = {}):
        self.name = name
        self.title = title
        self.slot = slot    # ex: 'main_hand', 'head'
        self.base_dmg = base_dmg
        self.dmg_type = dmg_type
        self.modifiers = modifiers

    def get_base_dmg(self) -> str:
        return self.base_dmg

    def get_modifiers(self):
        return self.modifiers.copy()
    
    def to_dict(self):
        return {
            'name': self.name,
            'title': self.title,
            'base_dmg': self.base_dmg,
            'slot': self.slot,
            'modifiers': self.modifiers
        }

    def __repr__(self):
        return f'{self.name}{f' ({self.title})' if self.title else ''}'

class EmptySlot(Equipment):
    def __init__(self, slot: str):
        base_dmg = '1d2' if slot in ['main_hand', 'off_hand'] else '0'
        super().__init__(name='Nothing', title='', base_dmg=base_dmg, dmg_type='bludgeoning', slot=slot, modifiers={})

    def __repr__(self):
        # Pode exibir “None (Empty)” ou apenas “None”
        return 'Nothing'