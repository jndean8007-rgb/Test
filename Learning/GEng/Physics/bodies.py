
class Bodies:
    def __init__(self, center, velocity, mass, elasticity, shape, angles, engine, game, id):
        self.properties = {'center' : center,
                                               'velocity' : velocity,
                                               'mass' : mass,
                                               'elasticity' : elasticity,
                                               'shape' : shape,
                                               'angles' : angles,
                                               'engine' : engine,
                                               'game' : game,
                                               'type' : 'Body',
                                               'id' : id}

    # define positional, rendering, and collision logic for each body