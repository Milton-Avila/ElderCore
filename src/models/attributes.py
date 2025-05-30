class Attributes:
    DEFAULT_SCORE = 8
    ATTR_NAMES = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']

    def __init__(self, **kwargs):
        for attr in self.ATTR_NAMES:
            setattr(self, attr, kwargs.get(attr, self.DEFAULT_SCORE))

    def __repr__(self):
        return f'{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in self.to_dict().items())})'

    def to_dict(self):
        return {attr: getattr(self, attr) for attr in self.ATTR_NAMES}
