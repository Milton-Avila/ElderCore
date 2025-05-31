class AttributeModifiers:
    def __init__(self, **kwargs):
        for attr in kwargs:
            setattr(self, attr)

    def __repr__(self):
        return f'{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in self.to_dict().items())})'

    def to_dict(self):
        return {attr: getattr(self, attr) for attr in dir(self) if not attr.startswith('__')}


class Equipment:
    def __init__(self, name: str, type: str, title: str, modifiers: AttributeModifiers):
        self.name = name
        self.type = type
        self.title = title
        self.modifiers = modifiers

    def __str__(self):
        return f'{self.name}: {self.title}'


class EquipmentSet:
    def __init__(self):
        self.head: Equipment = None
        self.main_hand: Equipment = None
        self.off_hand: Equipment = None

    def add_equipment(self, slot: str, item: Equipment):
        setattr(self, slot, item)

    def remove_equipment(self, slot: str):
        setattr(self, slot, None)