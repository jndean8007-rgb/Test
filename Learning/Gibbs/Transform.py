import numpy as np

class Renderer:

    def __init__(self, scale, angles, center, canvas_size = 800):
        self.scale = scale
        self.angles = angles
        self.center = center
        self.canvas_size = 800

    def set_angle(self, angles):
        self.angles = angles

    def set_scale(self, scale):
        self.scale = scale

    def transform(self, coords): #output x, y coord
        coords = np.asarray(coords, dtype=float)

        # Translate the point relative to the world-space center.
        c_t = coords - self.center

        theta, phi = self.angles

        right = np.array([
            np.sin(theta),
            -np.cos(theta),
            0
        ])

        up = np.array([
            -np.sin(phi) * np.cos(theta),
            -np.sin(theta) * np.sin(phi),
            np.cos(phi)
        ])

        xc = np.dot(c_t, right)
        yc = np.dot(c_t, up)

        # Convert projected coordinates into canvas coordinates.
        screen_x = self.canvas_size / 2 + self.scale * xc
        screen_y = self.canvas_size / 2 - self.scale * yc

        return screen_x, screen_y