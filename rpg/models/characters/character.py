from rpg.models.entity.equipment import Equipment
from rpg.models.entity.entity import Entity


class Character(Entity):
    def __init__(self, name:str, title:str, level:int, attrs_data:dict[str, int], equip_data:list[dict]):
        self.name = name
        self.title = title
        self._level = level
        self._attrs_data = attrs_data
        self._equip_data = equip_data
        
        super().__init__()
        self._equipment = Equipment(self._equip_data)

    @property
    def bio(self) -> dict:
        return {
            'name': self.name,
            'title': self.title,
            'char_sheet': self.char_sheet.to_dict()
        }

    @property
    def equipment(self) -> Equipment:
        return self._equipment

    @property
    def base_dmg(self):
        return self.main_weapon.base_dmg

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'title': self.title,
            'level': self._level,
            'attrs_data': {k: v for k, v in self.attrs_dict.items() if v != 8},
            'equip_data': self._equipment.to_dict()
        }
