class Equipment:
    def __init__(self, name: str, title: str, slot: str, modifiers: dict[str, int] = {}):
        self.name = name
        self.title = title
        self.slot = slot    # ex: 'main_hand', 'head'
        self.modifiers = modifiers

    def get_modifiers(self):
        return self.modifiers.copy()
    
    def to_dict(self):
        return {
            "name": self.name,
            "title": self.title,
            "slot": self.slot,
            "modifiers": self.modifiers
        }

    def __repr__(self):
        return f"{self.name}{f' ({self.title})' if self.title else ''}"

class EmptySlot(Equipment):
    def __init__(self, slot: str):
        super().__init__(name='Nothing', title='', slot=slot, modifiers={})

    def __repr__(self):
        # Pode exibir “None (Empty)” ou apenas “None”
        return "Nothing"