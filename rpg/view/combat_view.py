import re

# Cores ANSI
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

LINE_LEN = 60
ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

def strip_ansi(text):
    return ansi_escape.sub('', text)

def render_combat_banner(title: str) -> str:
    return f"{GREEN}{'┌' + f' {title} '.center(LINE_LEN, '─') + '┐'}{RESET}"

def render_combat_line(left: str = "", right: str = "") -> str:
    visible_left = strip_ansi(left)
    visible_right = strip_ansi(right)
    spacing = LINE_LEN - len(visible_left) - len(visible_right) - 4
    spacing = max(spacing, 0)
    return f"{GREEN}│ {RESET}{left}{' ' * spacing}{right}{GREEN} │{RESET}"

def render_combat_footer() -> str:
    return f"{GREEN}{'└' + '─' * LINE_LEN + '┘'}{RESET}"

def generate_bar(current: int, max_val: int, width: int = 28) -> str:
    filled = int((current / max_val) * width)
    empty = width - filled
    bar = f"{RED}{'█' * filled}{RESET}{'░' * empty}"
    return bar

def render_entity_status(ent, is_player: bool = True) -> list[str]:
    theme = GREEN if is_player else MAGENTA
    lines = []
    name_str = f"{theme}⚔ {ent.name.center(LINE_LEN - 4)} ⚔{RESET}"
    lines.append(render_combat_line(name_str))

    hp_bar = generate_bar(ent.hp_current, ent.hp_max)
    hp_line = f"{RED}{RESET}{hp_bar} {ent.hp_current}/{ent.hp_max}"
    lines.append(render_combat_line(hp_line))

    ac_line = f"{BLUE}🛡 AC: {ent.ac}{RESET}"
    lines.append(render_combat_line("", ac_line))

    if hasattr(ent, "states") and ent.states:
        state_line = f"{YELLOW}⚠ {', '.join(ent.states)}{RESET}"
        lines.append(render_combat_line(state_line))

    lines.append(render_combat_line())  # Empty spacer line
    return lines

def show_combat_status(*entities) -> None:
    print(render_combat_banner("Status de Combate"))
    for ent in entities:
        is_player = getattr(ent, "is_player", True)
        for line in render_entity_status(ent, is_player=is_player):
            print(line)
    print(render_combat_footer())