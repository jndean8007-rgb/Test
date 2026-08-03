from Sampler import GibbsSampler
import numpy as np
import tkinter as tk
from Transform import Renderer

class GibbsVisual:

    def __init__(self, gibbs, lag, center, scale, size = 800, speed = 100):
        self.Gibbs = gibbs
        self.lag = lag
        self.center = center
        self.scale = scale
        self.size = size
        self.speed = speed
        self.running = False
        self.shapes = []
        self.ids = []
        self.angles = [0,0]
        self.Renderer = Renderer(self.scale, self.angles, self.center, self.size)
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
        self.window.bind("<MouseWheel>", self.zoom)
        self.window.bind("<w>", self.forward)
        self.window.bind("<s>", self.backward)
        self.window.bind("<a>", self.left)
        self.window.bind("<d>", self.right)

        self.draw()

    def draw(self):
        means = np.asarray(self.Gibbs.get_means())
        covs = np.asarray(self.Gibbs.get_cov())

        if len(means) < 2 or len(covs) < 2:
            return

        # Produces one trace for every covariance matrix.
        covtrace = np.trace(covs, axis1=-2, axis2=-1)

        true1 = np.array([
            means[-2, 0],
            means[-2, 1],
            covtrace[-2]
        ])

        true2 = np.array([
            means[-1, 0],
            means[-1, 1],
            covtrace[-1]
        ])

        x1, y1 = self.Renderer.transform(true1)
        x2, y2 = self.Renderer.transform(true2)

        line_id = self.canvas.create_line(
            x1, y1,
            x2, y2,
            fill="white",
            width=2
        )

        self.shapes.append((true1, true2))
        self.ids.append(line_id)

        # Remove the oldest line after adding the newest.
        if len(self.shapes) > self.lag:
            self.shapes.pop(0)
            old_id = self.ids.pop(0)
            self.canvas.delete(old_id)

    def redraw(self):
        for line_id, (true1, true2) in zip(self.ids, self.shapes):
            x1, y1 = self.Renderer.transform(true1)
            x2, y2 = self.Renderer.transform(true2)

            self.canvas.coords(
                line_id,
                x1, y1,
                x2, y2
            )

        self.canvas.delete("grid")
        self.grid()
        self.canvas.tag_lower("grid")

    def grid(self):
        extent = 1

        axes = [
            (
                self.center + np.array([-extent, 0, 0]),
                self.center + np.array([ extent, 0, 0])
            ),
            (
                self.center + np.array([0, -extent, 0]),
                self.center + np.array([0,  extent, 0])
            ),
            (
                self.center + np.array([0, 0, -extent]),
                self.center + np.array([0, 0,  extent])
            )
        ]

        for start, end in axes:
            x1, y1 = self.Renderer.transform(start)
            x2, y2 = self.Renderer.transform(end)

            self.canvas.create_line(
                x1, y1, x2, y2,
                fill="gray",
                tags="grid"
            )

    def on_start_drag(self, event):
        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y
        self.drag_data['Item'] = self.canvas.find_closest(event.x, event.y)[0]

    def on_drag(self, event):
        dx = event.x - self.drag_data['x']
        dy = event.y - self.drag_data['y']

        self.angles[0] += 2 * dx / self.size
        self.angles[1] += 2 * dy / self.size

        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y

        self.Renderer.set_angle(self.angles)
        self.redraw()

    def on_drop(self, event):
        self.drag_data = {"x": 0, "y": 0, "item": None}

    def zoom(self, event):
        if event.delta > 0:
            self.scale *= 1.1

        if event.delta < 0:
            self.scale *= 0.9

        self.Renderer.set_scale(self.scale)
        self.redraw()

    def left(self, event):
        self.angles[0] -= np.pi / 16
        self.Renderer.set_angle(self.angles)
        self.redraw()

    def right(self, event):
        self.angles[0] += np.pi / 16
        self.Renderer.set_angle(self.angles)
        self.redraw()

    def backward(self, event):
        self.scale *= 0.9
        self.Renderer.set_scale(self.scale)
        self.redraw()

    def forward(self, event):
        self.scale *= 1.1
        self.Renderer.set_scale(self.scale)
        self.redraw()

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