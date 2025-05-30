from ..models.dice_controller import _DiceController

def get_range(dice_str: str) -> int:
    return _DiceController.get_range(dice_str)

def get_statistics() -> int:
    return _DiceController.get_statistics()