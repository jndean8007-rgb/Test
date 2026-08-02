from Sampler import GibbsSampler
import numpy as np
import tkinter as tk
from Transform import Renderer

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
        self.angles = [0,0]
        self.Renderer = Renderer(self.scale, self.angles)
        self.drag_data = {'x' : 0, 'y' : 0, 'Item' : None}

        self.window = tk.Tk()
        self.window.title("Gibbs Visual")
        self.window.configure(background="black")
        self.window.resizable(width=False, height=False)

        self.canvas = tk.Canvas(
            self.window,
            width = self.size,
            height = self.size,
            bg = "black",
            highlightthickness = 0,
        )
        self.canvas.pack(padx = 10, pady = 10)

        self.instructions = tk.Label(
            self.window,
            text="Space: play/pause    N: next iteration    Esc: close",
            bg="white",
            fg="black",
        )
        self.instructions.pack(pady=(0, 12))

        self.window.bind("<space>", self.toggle)
        self.window.bind("n", self.next_iter)
        self.window.bind("<Escape>", self.close)
        self.window.bind("<ButtonPress-1>", self.on_start_drag)
        self.window.bind("<B1-Motion>", self.on_drag)
        self.window.bind("<ButtonRelease-1>", self.on_drop)
        #self window bind scroll zoom

        self.draw()

    def draw(self):
        if self.shapes.__len__() > self.lag:
            self.canvas.delete(self.shapes.pop(0))

        means = self.Gibbs.get_means()
        covtrace = np.trace(self.Gibbs.get_cov())

        if len(means) >= 2:
            x1, y1 = self.Renderer.transform((means[-2] - self.center[0:2], covtrace[-2] - self.center[3]))
            x2, y2 = self.Renderer.transform((means[-1] - self.center[0:2], covtrace[-1] - self.center[3]))

            line = self.canvas.create_line(
                x1, y1,
                x2, y2,
                fill = "white",
                width = 2
            )

            self.shapes.append(line)

    def grid(self):

        lx1 = (-1, 0, 0)
        ly1 = (0, -1, 0)
        lz1 = (0, 0, -1)

        lx2 = (1, 0, 0)
        ly2 = (0, 1, 0)
        lz2 = (0, 0, 1)

        self.canvas.create_line(self.Renderer.transform(lx1), self.Renderer.transform(lx2))
        self.canvas.create_line(self.Renderer.transform(ly1), self.Renderer.transform(ly2))
        self.canvas.create_line(self.Renderer.transform(lz1), self.Renderer.transform(lz2))

    def on_start_drag(self, event):
        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y
        self.drag_data['Item'] = self.canvas.find_closest(event.x, event.y)[0]

    def on_drag(self, event):
        dx = event.x - self.drag_data['x']
        dy = event.y - self.drag_data['y']

        self.Renderer.angles(angles)

    def on_drop(self, event):
        self.drag_data = {"x": 0, "y": 0, "item": None}


    def zoom(self):
        #---
        #zoom functionality
        #---
        self.Renderer.scale(scale)

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