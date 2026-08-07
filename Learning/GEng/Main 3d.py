from Physics import Game
import json
from pathlib import Path

#make startup portable

def main():
    cwd = Path.cwd()
    filepath = cwd / "3d_data.json"
    game = Game.Game(800, 600, 60, filepath)

if __name__ == '__main__':
    main()