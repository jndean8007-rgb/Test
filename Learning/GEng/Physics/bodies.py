import numpy as np

class Bodies:
    def __init__(self, center, dimensions, velocity, mass, elasticity, shape, angles, engine, game, id):
        self.type = "Body"
        self.properties = {
            "center": np.asarray(center, dtype=float),
            "dimensions": np.asarray(dimensions, dtype=float),
            "velocity": np.asarray(velocity, dtype=float),
            "mass": float(mass),
            "elasticity": float(elasticity),
            "shape": shape,
            "angles": np.asarray(angles, dtype=float),
            "engine": engine,
            "game": game,
            "type": self.type,
            "id": id,
        }

        if self.properties['shape'] == 'rectangle':
            self.edges = [
                (0, 1), (0, 2), (0, 4),
                (1, 3), (1, 5),
                (2, 3), (2, 6),
                (3, 7),
                (4, 5), (4, 6),
                (5, 7),
                (6, 7),
            ]
            hx, hy, hz = self.half_extents

            self.local_vertices = np.array([
                [-hx, -hy, -hz],
                [hx, -hy, -hz],
                [-hx, hy, -hz],
                [hx, hy, -hz],
                [-hx, -hy, hz],
                [hx, -hy, hz],
                [-hx, hy, hz],
                [hx, hy, hz],
            ])
            self.vertices = self.world_vertices()

        elif self.properties['shape'] == 'tetrahedron':
            self.edges = [
                (0, 1), (0, 2), (0, 3),
                (1, 2), (1, 3),
                (2, 3),
            ]

            self.local_vertices = np.array([
                [1, 1, 1],
                [-1, -1, 1],
                [-1, 1, -1],
                [1, -1, -1],
            ], dtype=float)

            self.local_vertices *= self.properties['dimensions']
            self.vertices = self.world_vertices()

        elif self.properties['shape'] == 'sphere':
            self.radius = float(self.properties['dimensions'].item())

    @property
    def half_extents(self):
        return np.asarray(
            self.properties["dimensions"],
            dtype=float,
        ) / 2

    @property
    def rotation_matrix(self):
        angles = np.asarray(
            self.properties["angles"],
            dtype=float,
        )

        angle_x, angle_y, angle_z = angles

        cos_x, sin_x = np.cos(angle_x), np.sin(angle_x)
        cos_y, sin_y = np.cos(angle_y), np.sin(angle_y)
        cos_z, sin_z = np.cos(angle_z), np.sin(angle_z)

        rotation_x = np.array([
            [1, 0, 0],
            [0, cos_x, -sin_x],
            [0, sin_x, cos_x],
        ])

        rotation_y = np.array([
            [cos_y, 0, sin_y],
            [0, 1, 0],
            [-sin_y, 0, cos_y],
        ])

        rotation_z = np.array([
            [cos_z, -sin_z, 0],
            [sin_z, cos_z, 0],
            [0, 0, 1],
        ])

        return rotation_z @ rotation_y @ rotation_x

    def world_vertices(self):
        local_vertices = self.local_vertices
        rotation = self.rotation_matrix
        center = self.properties["center"]

        return local_vertices @ rotation.T + center

    #def is_clicked(self):
    # define is_clicked
    #def is_x(self)
    #def in_reach(self):