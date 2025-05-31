from src.models.character import Character
from src.packages.char_sheet import EQUIPMENT_SLOTS

def display_character_sheet(char_list: list[Character]):
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

    for char in char_list:
        line_len = 74
        header = f' Biography '
        border_top = GREEN + '┌' + header.center(line_len, '─') + '┐' + RESET
        border_attr = GREEN + '├' + ' Attributes '.center(line_len, '─') + '┤' + RESET
        border_eq = GREEN + '├' + ' Equipment '.center(line_len, '─') + '┤' + RESET
        border_bottom = GREEN + '└' + '─' * line_len + '┘' + RESET

        print(border_top)
        print(f'{GREEN}│{RESET} {RED}Name{RESET}         : {char.name:<58}{GREEN}│{RESET}')
        print(f'{GREEN}│{RESET} {RED}Title{RESET}        : {char.title:<58}{GREEN}│{RESET}')
        print(border_attr)

        base_attrs = char.attributes.to_dict()
        bonuses = char.get_equipment_attr_bonus()
        attr_names = list(base_attrs.keys())

        for i in range(0, len(attr_names), 3):
            chunk = attr_names[i:i+3]
            line = ''
            for j, attr in enumerate(chunk):
                base_val = base_attrs[attr]
                bonus_val = bonuses.get(attr, 0)
                bonus_str = f' (+{bonus_val})' if bonus_val > 0 else f'     '
                line += f'{RED}{attr.capitalize():<13}{RESET}: {base_val:>2}{bonus_str}'
                if j < len(chunk) - 1:
                    line += '   '
            print(f'{GREEN}│ {line:<77} {GREEN}│{RESET}')

        print(border_eq)
        for slot in EQUIPMENT_SLOTS:
            label = slot.replace("_", " ").title()
            item = char.equipment.get(slot)
            name = str(item) if item else 'None'
            print(f'{GREEN}│{RESET} {RED}{label:<13}{RESET}: {name:<58}{GREEN}│{RESET}')

        print(border_bottom)