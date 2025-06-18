from rpg.models.entity.equipment import Equipment
from rpg.models.entity.item import EMPTY_SLOT
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
    def main_weapon(self):
        return self.equipment.main_weapon
    
    @property
    def off_hand(self):
        return self.equipment.off_hand

    @property
    def base_dmg(self):
        return self.main_weapon.base_dmg

    # def choose_action(self, allies: list[Entity], enemies: list[Entity], aggro: AggroSystem) -> Action:
    #     def choose_target(targets: List[Entity]) -> Entity:
    #         for i, target in enumerate(targets, 1):
    #             print(f"{i}. {target.describe()}")
    #         while True:
    #             try:
    #                 idx = int(input("Choose a target: ")) - 1
    #                 return targets[idx]
    #             except (ValueError, IndexError):
    #                 print("Invalid choice, try again.")

    #     print(f"{self.name}'s turn. Choose an action:")
    #     print('1. Attack\n2. Defend\n3. Skills\n4. Use Item')
    #     while True:
    #         match input('> '):
    #             case '1':
    #                 return self.attack(choose_target(enemies))
    #             case '2':
    #                 return self.defend()
    #             case '3':
    #                 return self.use_skill()
    #             case '4':
    #                 return self.use_item()
    #             case _:
    #                 print("Invalid choice.")

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'title': self.title,
            'level': self._level,
            'attrs_data': {k: v for k, v in self.char_sheet.attrs.to_dict().items() if v != 8},
            'equip_data': self._equipment.to_dict()
        }
