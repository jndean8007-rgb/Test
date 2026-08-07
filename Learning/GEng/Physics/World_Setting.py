import numpy as np

class World_Setting:
    def __init__(self, dimensions, shape, elasticity): #much later add different types of world such as sphere etc and perhaps more complicated settings
        self.dimensions = dimensions
        self.properties = {"type" : 'World_Settings',
                           'dimensions' : np.asarray(dimensions, dtype = float),
                           'mass' : 0,
                           'shape' : shape,
                           'elasticity' : float(elasticity)}
        self.vertices = []
        self.is_static = True

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
            x, y, z = self.properties['dimensions']

            self.vertices = [
                [0, 0, 0],
                [x, 0, 0],
                [0, y, 0],
                [x, y, 0],
                [0, 0, z],
                [x, 0, z],
                [0, y, z],
                [x, y, z],
            ]
    #def isoutside