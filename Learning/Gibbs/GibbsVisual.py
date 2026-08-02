from Sampler import GibbsSampler
import tkinter as tk

class GibbsVisual:

    def __init__(self, gibbs, lag, center, scale,size = 800, speed = 100):
        self.Gibbs = gibbs
        self.lag = lag
        self.center = center
        self.scale = scale
        self.size = size
        self.speed = speed
        self.running = False
        self.shapes = []

        self.window = tk.Tk()
        self.window.title("Gibbs Visual")
        self.window.configure(background="white")
        self.window.resizable(width=False, height=False)

        self.canvas = tk.Canvas(
            self.window,
            width = self.size,
            height = self.size,
            bg = "white",
            highlightthickness = 0,
        )

        self.canvas.pack(padx = 10, pady = 10)

        self.instructions = tk.Label(
            self.window,
            text="Space: play/pause    N: next iteration    Esc: close",
            bg="black",
            fg="white",
        )
        self.instructions.pack(pady=(0, 12))

        self.window.bind("<space>", self.toggle)
        self.window.bind("n", self.next_iter)
        self.window.bind("<Escape>", self.close)

        self.draw()

    def draw(self):
        if self.shapes.__len__() > self.lag:
            self.canvas.delete(self.shapes.pop(0))

        means = self.Gibbs.get_means()
        if len(means) >= 2:
            x1, y1 = self.to_canvas(means[-2])
            x2, y2 = self.to_canvas(means[-1])

            line = self.canvas.create_line(
                x1, y1,
                x2, y2,
                fill = "black",
                width = 2
            )

            self.shapes.append(line)

    def to_canvas(self, point):
        x, y = point

        canvas_x = self.size / 2 + (x - self.center[0]) * self.scale
        canvas_y = self.size / 2 - (y - self.center[1]) * self.scale

        return canvas_x, canvas_y

    def grid(self):
        self.canvas.create_line(self.size / 2, 0, self.size / 2, self.size)
        self.canvas.create_line(0, self.size / 2, self.size, self.size / 2)

        for i in range(9):
            self.canvas.create_line((i+1) * self.size/10, 0, (i+1) * self.size/10, self.size)

        for j in range(9):
            self.canvas.create_line(0, (j+1)*self.size/10, self.size, (j+1)*self.size/10)

    def loop(self):
        if self.running:
            self.Gibbs.sample()
            self.draw()

        self.window.after(self.speed, self.loop)

    def toggle(self, event=None):
        self.running = not self.running

    def close(self, event=None):
        self.window.destroy()

    def next_iter(self, event=None):
        if not self.running:
            self.Gibbs.sample()
            self.draw()

    def start(self):
        self.grid()
        self.loop()
        self.window.mainloop()