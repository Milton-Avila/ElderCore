
import os

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def pause(message: str = ''):
    clear()
    input(f'{message}\nPress Enter to continue...')
    clear()