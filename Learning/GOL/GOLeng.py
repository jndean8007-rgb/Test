import tkinter as tk

class GameEngine:
    def __init__(self, state, cell_size = 25, speed = 100):
        self.state = state
        self.cell_size = cell_size
        self.speed = speed
        self.running = False

        self.window = tk.Tk()
        self.window.title("GOL")
        self.window.configure(bg = '#202020')
        self.window.resizable(width=False, height=False)

        self.canvas = tk.Canvas(
            self.window,
            width = self.state.x * self.cell_size,
            height = self.state.y * self.cell_size,
            bg = '#111111',
            highlightthickness = 0
        )

        self.canvas.pack(padx = 15, pady = 15)

        self.instructions = tk.Label(
            self.window,
            text="Space: play/pause    N: next generation    Esc: close",
            bg="#202020",
            fg="white",
        )
        self.instructions.pack(pady=(0,12))

        self.window.bind("<space>", self.toggle)
        self.window.bind("n", self.next_generation)
        self.window.bind("<Escape>", self.close)

        self.draw()

    def draw(self):
        self.canvas.delete("all")

        for row in range(self.state.y):
            for col in range(self.state.x):
                cell = self.state.get(row, col)

                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "#70e1a1" if cell.alive else '#171717'

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='#303030')

    def loop(self):
        if self.running:
            self.state.cont()
            self.draw()

        self.window.after(self.speed, self.loop)

    def toggle(self, event=None):
        self.running = not self.running

    def close(self, event=None):
        self.window.destroy()

    def next_generation(self, event=None):
        if not self.running:
            self.state.cont()
            self.draw()

    def start(self):
        self.loop()
        self.window.mainloop()



