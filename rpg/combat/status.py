from rpg.models.entity import Entity

class StatusSystem:
    @staticmethod
    def apply_effects(entity: Entity):
        for effect in entity.status_effects:
            effect.apply(entity)
        entity.cleanup_expired_effects()