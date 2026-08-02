import random

class Cell:

    def __init__(self, state, loc):
        self.group = state
        self.loc = loc
        self.stat = 1 if random.random() < state.p else 0

    def __repr__(self):
        return str(self.stat)

    def __eq__(self, other):
        return self.stat == other

    def edges(self, way, direction):
        column, row = self.loc

        if way == "Vertical":
            if direction == "+":
                return (row + 1) % self.group.y
            return (row - 1) % self.group.y

        if direction == "+":
            return (column + 1) % self.group.x
        return (column - 1) % self.group.x

    def next_status(self):
        column, row = self.loc

        row_above = self.edges("Vertical", "-")
        row_below = self.edges("Vertical", "+")
        column_left = self.edges("Horizontal", "-")
        column_right = self.edges("Horizontal", "+")

        neighbors = [
            self.group.get(column_left, row),
            self.group.get(column_right, row),

            self.group.get(column_left, row_above),
            self.group.get(column, row_above),
            self.group.get(column_right, row_above),

            self.group.get(column_left, row_below),
            self.group.get(column, row_below),
            self.group.get(column_right, row_below),
        ]

        count = sum(cell.stat for cell in neighbors)

        if self.stat == 1:
            return 1 if count in (2, 3) else 0

        return 1 if count == 3 else 0



class States:

    def __init__(self, x, y, p):
        self.x = x
        self.y = y
        self.p = p
        self.state = [[Cell(self, (col,row)) for col in range(x)] for row in range(y)]

    def get(self, y, x):
        return self.state[x][y]

    def get_cell(self, y, x):
        return self.state[x][y]

    def __repr__(self):
        alive = sum(cell.stat for row in self.state for cell in row)
        dead = self.x * self.y - alive
        return f'{alive} alive and {dead} dead.'

    def cont(self):
        next_stats= [
            [cell.next_status() for cell in row]
            for row in self.state
        ]

        for row in range(self.y):
            for col in range(self.x):
                self.state[row][col].stat = next_stats[row][col]

        return self
state = States(10,9,0.5)
for i in range(15):
    print(state.cont())


#rendering states through tkinter (note to self)#