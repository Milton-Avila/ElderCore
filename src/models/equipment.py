class Equipment:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __repr__(self):
        return f'Equipment(name={self.name}, description={self.description})'

    def __str__(self):
        return f'{self.name}: {self.description}'