from ..models.dice_controller import _DiceController

def roll(dice_str: str, possible_crit: bool = False) -> dict:
    return _DiceController.roll(dice_str, possible_crit)