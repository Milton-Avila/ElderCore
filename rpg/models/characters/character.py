from rpg.models.base.equipment import Equipment
from rpg.models.base.item import EMPTY_SLOT
from rpg.models.base.entity import Entity


class Character(Entity):
    def __init__(self, name:str, title:str, level:int, attrs_data:dict[str, int], equip_data:list[dict]):
        self.name = name
        self.title = title
        self.level = level
        self.attrs_data = attrs_data
        self.equip_data = equip_data
        
        super().__init__()
        self.equipment = Equipment(self.equip_data)

    @property
    def bio(self) -> dict:
        return {
            'name': self.name,
            'title': self.title,
            'char_sheet': self.char_sheet.to_dict()
        }

    # @property
    # def base_dmg(self) -> int:
    #     weapon = self.main_weapon
    #     return weapon.base_dmg if weapon != EMPTY_SLOT else 1

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
            'level': self.level,
            'attrs_data': {k: v for k, v in self.char_sheet.attrs.to_dict().items() if v != 8},
            'equip_data': self.equipment.to_dict()
        }
