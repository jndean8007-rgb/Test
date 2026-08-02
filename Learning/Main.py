import Life
import GOLeng

def main():

    state = Life.States(30, 30, 0.3)
    game = GOLeng.GameEngine(state, cell_size = 25, speed= 100)

    game.start()

if __name__ == '__main__':
    main()