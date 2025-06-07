import random

from .errors import InvalidDiceNotation
from .dice_input import _DiceInfo

class _DiceController:
    _dice_rolled: int = 0

    @classmethod
    def roll(cls, dice_str: str, possible_crit: bool = False) -> dict:
        def simple_roll(max: int) -> int:
            return random.randint(1, max)

        cls._dice_rolled += 1

        dice_info = _DiceInfo(dice_str)

        result_sum = 0
        individual_rolls = []
        crit_status = None

        for die in dice_info.get_dice_list():
            for _ in range(die['rolls']):
                roll = simple_roll(die['type'])
                individual_rolls.append((roll, die['type']))
                result_sum += roll

        total = result_sum + dice_info.get_bonus()

        if possible_crit:
            if len(individual_rolls) == 1:
                roll, die_type = individual_rolls[0]
                if die_type == 20:
                    if roll == 20:
                        crit_status = 'CRITICAL_SUCCESS'
                    elif roll == 1:
                        crit_status = 'CRITICAL_FAILURE'

        return {
            'result': total,
            'crit': crit_status,
            'rolls': individual_rolls,
            'bonus': dice_info.get_bonus()
        }

    @staticmethod
    def get_range(dice_str) -> dict:
        dice_info = _DiceInfo(dice_str)

        min_val = sum([die['rolls'] for die in dice_info.get_dice_list()]) + dice_info.get_bonus()
        max_max = sum([die['rolls'] * die['type'] for die in dice_info.get_dice_list()]) + dice_info.get_bonus()

        return {
            'min': min_val,
            'max': max_max
        }

    @classmethod
    def get_statistics(cls) -> dict[str, int]:
        return {
            'rolls': cls._dice_rolled
        }
