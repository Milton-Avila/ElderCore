from rpg.models.base.entity import Entity

class StatusSystem:
    @staticmethod
    def apply_effects(entity: Entity):
        for effect in entity.status_effects:
            effect.apply(entity)
        entity.cleanup_expired_effects()