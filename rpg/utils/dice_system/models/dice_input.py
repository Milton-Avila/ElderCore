from dataclasses import dataclass, field
from typing import List, Dict
import re

from .errors import InvalidDiceNotation

@dataclass
class _DiceInfo:
    dice_str: str
    _dice_list: List[Dict[str, int]] = field(init=False)
    _bonus: int = field(init=False)

    def __post_init__(self):
        self._dice_list, self._bonus = self._dice_str_interpreter(self.dice_str)

    def get_dice_list(self) -> List[Dict[str, int]]:
        return self._dice_list

    def get_bonus(self) -> int:
        return self._bonus
    
    @staticmethod
    def _dice_str_interpreter(dice_str: str) -> tuple[list[dict[str, int]], int]:
        cleaned = dice_str.replace(" ", "")

        if not cleaned:
            raise InvalidDiceNotation(dice_str)

        # Corrige sinais duplos, tipo "+-2" → "-2"
        cleaned = re.sub(r'([+-])([+-])', lambda m: '-' if m.group(1) == m.group(2) else '+', cleaned)

        # Garante que começa com sinal
        if cleaned[0] not in "+-":
            cleaned = "+" + cleaned

        # Valida com padrão ajustado
        valid_pattern = r'^([+-](\d+d\d+|\d+))+$'
        if not re.fullmatch(valid_pattern, cleaned):
            raise InvalidDiceNotation(dice_str)

        # Divide nos tokens (sinal + valor)
        tokens = re.findall(r'([+-])(\d+d\d+|\d+)', cleaned)

        dice_list = []
        bonus = 0

        for sign, value in tokens:
            multiplier = 1 if sign == '+' else -1

            if 'd' in value:
                try:
                    rolls, d_type = map(int, value.lower().split('d'))
                    if rolls <= 0 or d_type <= 0:
                        raise InvalidDiceNotation(dice_str)
                    dice_list.append({
                        'rolls': rolls * multiplier,
                        'type': d_type
                    })
                except:
                    raise InvalidDiceNotation(dice_str)
            else:
                bonus += multiplier * int(value)

        if not dice_list:
            raise InvalidDiceNotation(dice_str)

        return dice_list, bonus