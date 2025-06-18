import time
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def slow_write(messages: str | list, delay: float = 0.07):
    if isinstance(messages, str):
        messages = [messages]
        
    for message in messages:
        for char in message:
            print(char, end='', flush=True)
            if char != '\n':
                time.sleep(delay)
                
        if message != messages[-1]:
            time.sleep(delay*15)
            print()

def pause(message: str = ''):
    clear_console()
    slow_write([f'{message}', 'Press Enter to continue...'])
    input()
    clear_console()