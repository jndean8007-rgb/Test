import random
import time
import keyboard
import os
#yapp


class cell:
    def __init__(self, state):
        self.state = state
        if random.random() <= state.p:
            self.stat = 0
    def __repr__(self):
        return str(self.stat)
    def __eq__(self, other):
        return self.stat == other.stat


class state:
    def _init__(self, x, y, p):
        self.x = x
        self.y = y
        self.p = p
        self.state = [[cell(self) * self.x] for _ in range(self.y)]



def dead_state(x, y):
    return [[0] * x for _ in range(y)]


def random_state(x, y):
    state = dead_state(x, y)

    for i in range(len(state)):
        for j in range(len(state[i])):
            if random.random() <= 0.4:
                state[i][j] = 1

    return state


def render(state):
    print('-' * (len(state[0]) * 3 + 2))

    for row in state:
        print('|', end='')

        for cell in row:
            if cell == 1:
                print(' o ', end='')
            else:
                print('   ', end='')

        print('|')

    print('-' * (len(state[0]) * 3 + 2))


def edges(index, direction, length):
    if direction == '+':
        return (index + 1) % length
    else:
        return (index - 1) % length


def next_board_state(state):
    rows = len(state)
    columns = len(state[0])

    # Create a separate board so state isn't modified while counting.
    next_board = dead_state(columns, rows)

    for i in range(rows):
        for j in range(columns):
            count = 0

            row_above = edges(i, '-', rows)
            row_below = edges(i, '+', rows)
            column_left = edges(j, '-', columns)
            column_right = edges(j, '+', columns)

            count += state[i][column_left]
            count += state[i][column_right]

            count += state[row_above][column_left]
            count += state[row_above][j]
            count += state[row_above][column_right]

            count += state[row_below][column_left]
            count += state[row_below][j]
            count += state[row_below][column_right]

            if state[i][j] == 1:
                if count == 2 or count == 3:
                    next_board[i][j] = 1
            else:
                if count == 3:
                    next_board[i][j] = 1

    return next_board


s1 = random_state(5, 10)
sn = next_board_state(s1)
try:
    while True:
        if keyboard.is_pressed('q'):
            break
        sn = next_board_state(sn)
        render(sn)
        time.sleep(0.05)
except KeyboardInterrupt:
    print('\nGoodbye')



# turn into CLASSES