import numpy as np
from Physics.forces import Force
import uuid


class Camera:
    def __init__(
        self,
        reach: int,
        start_settings: list,
        sensitivity: float,
    ):
        if len(start_settings) != 5:
            raise ValueError(
                "start_settings must contain theta, phi, x, y, and z"
            )

        self.reach = float(reach)
        self.settings = np.asarray(start_settings, dtype=float)
        self.sensitivity = float(sensitivity)

        self.type = "Camera"
        self.vz = 0.0

        self.update_vectors()

        self.force = Force(
            np.array([0.0, 0.0, -1.0]),
            9.8,
            self,
            None,
            "gravity",
            str(uuid.uuid4()),
        )

    def get_settings(self):
        return tuple(self.settings)

    @property
    def theta(self):
        return self.settings[0]

    @theta.setter
    def theta(self, value):
        self.settings[0] = float(value)
        self.update_vectors()

    @property
    def phi(self):
        return self.settings[1]

    @phi.setter
    def phi(self, value):
        self.settings[1] = float(
            np.clip(
                value,
                -np.pi / 2 + 0.01,
                np.pi / 2 - 0.01,
            )
        )
        self.update_vectors()

    @property
    def position(self):
        return self.settings[2:5]

    @position.setter
    def position(self, coordinates):
        coordinates = np.asarray(coordinates, dtype=float)

        if coordinates.shape != (3,):
            raise ValueError("Camera position must contain x, y, and z")

        self.settings[2:5] = coordinates

    def update_vectors(self):
        theta = self.theta
        phi = np.clip(
            self.phi,
            -np.pi / 2 + 0.01,
            np.pi / 2 - 0.01,
        )

        self.forward = np.array(
            [
                np.cos(phi) * np.sin(theta),
                np.cos(phi) * np.cos(theta),
                np.sin(phi),
            ],
            dtype=float,
        )

        self.right = np.array(
            [
                np.cos(theta),
                -np.sin(theta),
                0.0,
            ],
            dtype=float,
        )

        self.up = np.cross(self.right, self.forward)

        self.forward /= np.linalg.norm(self.forward)
        self.right /= np.linalg.norm(self.right)
        self.up /= np.linalg.norm(self.up)

    def relative_position(self, coordinates):
        coordinates = np.asarray(coordinates, dtype=float)
        return coordinates - self.position

    def rotate(self, rotation: list):
        self.settings[0] += rotation[0] * np.pi / 180 * self.sensitivity
        self.settings[1] += rotation[1] * np.pi / 180 * self.sensitivity

        self.settings[0] %= 2 * np.pi

        self.settings[1] = np.clip(
            self.settings[1],
            -np.pi / 2 + 0.01,
            np.pi / 2 - 0.01,
        )

        self.update_vectors()

    def move(self, displacement: list):
        if len(displacement) != 3:
            raise ValueError("displacement must contain x, y, and z")

        theta = self.settings[0]
        local_x, local_y, local_z = displacement

        world_x = local_x * np.cos(theta) - local_y * np.sin(theta)
        world_y = local_x * np.sin(theta) + local_y * np.cos(theta)

        self.settings[2] += world_x
        self.settings[3] += world_y
        self.settings[4] += local_z

    def integrate(self, dt: float):
        self.settings[4] += self.vz * dt
        if self.settings[4] <= 0:
            self.settings[4] = 0.0
            self.vz = 0.0

    def is_on(self):
        if self.settings[4] == 0: #improve to mean if on top of any object
            return True
        #if
