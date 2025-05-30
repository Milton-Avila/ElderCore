import os
from . import functions as dice

while True: 
    os.system('cls' if os.name == 'nt' else 'clear')
    dice_value = input('\nRoll a dice: ')
    print("\nResult: ", dice.roll(dice_value))
    print("Min and max values possible: ", dice.get_range(dice_value))
    print("Statistics: ", dice.get_statistics())
    input("\nPress Enter to roll again or Ctrl+C to exit.")