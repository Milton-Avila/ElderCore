class Action:
    def __init__(self, actor, name: str, type: str, description: str, effect: callable = None):
        self.actor = actor
        self.name = name
        self.type = type
        self.description = description
        self.effect = effect