class Equipment:
    def __init__(self, name: str, title: str, slot: str, base_dmg: str = None, modifiers: dict[str, int] = {}):
        self.name = name
        self.title = title
        self.slot = slot    # ex: 'main_hand', 'head'
        print(name)
        input(base_dmg)
        self.base_dmg = self.handle_base_dmg(base_dmg)
        self.modifiers = modifiers

    def get_base_dmg(self) -> str:
        return self.base_dmg

    def get_modifiers(self):
        return self.modifiers.copy()
    
    def to_dict(self):
        return {
            "name": self.name,
            "title": self.title,
            "base_dmg": self.base_dmg,
            "slot": self.slot,
            "modifiers": self.modifiers
        }
    
    def handle_base_dmg(self, base_dmg: str) -> str:
        if self.slot != 'head':
            return base_dmg
        else:
            return None

    def __repr__(self):
        return f"{self.name}{f' ({self.title})' if self.title else ''}"

class EmptySlot(Equipment):
    def __init__(self, slot: str):
        super().__init__(name='Nothing', title='', slot=slot, modifiers={})

    def __repr__(self):
        # Pode exibir “None (Empty)” ou apenas “None”
        return "Nothing"