import arcade
from game import TheGame

def main():
    
    game = TheGame(600, 600, "Game Title")
    arcade.run()

if __name__ == "__main__":
    main()