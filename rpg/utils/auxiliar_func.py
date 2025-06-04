
import os

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause(message: str = ''):
    cls()
    input(f'{message}\n\nPress Enter to continue...')
    cls()