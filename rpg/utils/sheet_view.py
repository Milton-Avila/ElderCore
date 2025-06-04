from rpg.models.character import Character
from rpg.packages import EQUIPMENT_SLOTS

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Helper lambdas
bio = lambda char: char.bio
base_attrs = lambda char: char.attributes.to_dict()
bonuses = lambda char: char.equipment_mod
attr_names = lambda char: list(base_attrs(char).keys())

# Line structure
line_len = 75

def border_top(char):
    return GREEN + '┌' + f" {bio(char)['title']} ".center(line_len, '─') + '┐' + RESET

def border_section(title):
    return GREEN + '├' + f' {title} '.center(line_len, '─') + '┤' + RESET

def border_bottom():
    return GREEN + '└' + '─' * line_len + '┘' + RESET

def format_attr_line(attr_chunk, base, bonus):
    line = ''
    for i, attr in enumerate(attr_chunk):
        base_val = base[attr]
        bonus_val = bonus.get(attr, 0)
        bonus_str = f'(+{bonus_val})' if bonus_val > 0 else '    '
        line += f'{RED}{attr.capitalize():<13}{RESET}: {base_val:>2}{bonus_str}'
        if i < len(attr_chunk) - 1:
            line += '     '
    return f'{GREEN}│ {line:<{line_len}} {GREEN}│{RESET}'

def render_equipment_line(slot, item):
    label = slot.replace("_", " ").title()
    name = str(item) if item else 'None'
    return f'{GREEN}│{RESET} {RED}{label:<13}{RESET}: {name:<59}{GREEN}│{RESET}'

def _render_character_lines(char):
    bio_data = bio(char)
    base = base_attrs(char)
    bonus = bonuses(char)
    attrs = attr_names(char)

    lines = [
        border_top(char),
        f'{GREEN}│{RESET} {RED}Name{RESET}         : {bio_data["name"]:<34}   {RED}Max HP{RESET}       : {bio_data["combat_stats"]["hp_max"]:>2}     {GREEN}│{RESET}',
        f'{GREEN}│{RESET} {RED}Level{RESET}        : {bio_data["level"]:>2}{"":<35}{RED}Max MP{RESET}       : {bio_data["combat_stats"]["hp_max"]-5:>2}{"":<4} {GREEN}│{RESET}',
        border_section("Vital Status")
    ]

    for i in range(0, len(attrs), 3):
        lines.append(format_attr_line(attrs[i:i+3], base, bonus))

    lines.append(border_section("Gear"))
    for slot in EQUIPMENT_SLOTS:
        item = char.get_equipment(slot)
        lines.append(render_equipment_line(slot, item))

    lines.append(border_bottom())
    return lines

def _display_vertical(char_list: list[Character]):
    for char in char_list:
        print("\n".join(_render_character_lines(char)))

def _display_horizontal(char_list: list[Character]):
    sheets = [_render_character_lines(char) for char in char_list]
    max_lines = max(len(sheet) for sheet in sheets)
    width = line_len + 2
    spacer = ' ' * 5

    # Normalize
    for sheet in sheets:
        sheet.extend([' ' * width] * (max_lines - len(sheet)))

    for lines in zip(*sheets):
        print(spacer.join(lines))

def display_character_sheet(char_list: list[Character], horizontal: bool = False):
    if horizontal:
        _display_horizontal(char_list)
    else:
        _display_vertical(char_list)
