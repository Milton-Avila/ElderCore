from src.core.RPGSystem import RPGSystem

def main():
    system = RPGSystem()
    system.setup()
    system.show_characters()

if __name__ == '__main__':
    main()