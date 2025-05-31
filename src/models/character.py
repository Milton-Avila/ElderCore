from src.packages.char_sheet import ATTR_NAMES
from src.models.equipment import EquipmentSet


class Character:
    def __init__(self, name: str, title: str, attributes: dict):
        self.name = name
        self.title = title
        self.attributes = Attributes(**attributes)
        self.equipment = EquipmentSet()

    def display(self):
        GREEN = "\033[92m"
        RED = "\033[91m"
        RESET = "\033[0m"

        line_len = 72
        header = f" Character Sheet "
        border_top = GREEN + "┌" + header.center(line_len, "─") + "┐" + RESET
        border_attr = GREEN + "├" + " Attributes ".center(line_len, "─") + "┤" + RESET
        border_eq = GREEN + "├" + " Equipment ".center(line_len, "─") + "┤" + RESET
        border_bottom = GREEN + "└" + "─" * line_len + "┘" + RESET

        print(border_top)
        print(f"{GREEN}│{RESET} {RED}Name{RESET}     : {self.name:<60}{GREEN}│{RESET}")
        print(f"{GREEN}│{RESET} {RED}Title{RESET}    : {self.title:<60}{GREEN}│{RESET}")
        print(border_attr)

        attrs = self.attributes.to_dict()
        attr_names = list(attrs.keys())
        for i in range(0, len(attr_names), 3):
            chunk = attr_names[i:i+3]
            line = ""
            for attr in chunk:
                val = f"{attrs[attr]:<3}"
                line += f"{RED}{attr.capitalize():<13}{RESET}: {val}     "
            print(f"{GREEN}│ {line:<77}  {GREEN}│{RESET}")

        print(border_eq)
        print(f"{GREEN}│{RESET} {RED}Head{RESET}        : {str(self.equipment.head or 'None'):<57}{GREEN}│{RESET}")
        print(f"{GREEN}│{RESET} {RED}Main Hand{RESET}   : {str(self.equipment.main_hand or 'None'):<57}{GREEN}│{RESET}")
        print(f"{GREEN}│{RESET} {RED}Off Hand{RESET}    : {str(self.equipment.off_hand or 'None'):<57}{GREEN}│{RESET}")
        print(border_bottom)



class Attributes:
    DEFAULT_SCORE = 8

    def __init__(self, **kwargs):
        for attr in ATTR_NAMES:
            setattr(self, attr, kwargs.get(attr, self.DEFAULT_SCORE))

    def to_dict(self):
        return {attr: getattr(self, attr) for attr in ATTR_NAMES}