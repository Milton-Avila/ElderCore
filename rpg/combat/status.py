class StatusSystem:
    @staticmethod
    def apply_effects(character):
        for effect in character.status_effects:
            effect.apply(character)
        character.cleanup_expired_effects()