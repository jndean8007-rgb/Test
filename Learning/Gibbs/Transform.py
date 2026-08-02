
class Renderer:

    def __init__(self, scale, angles):
        self.scale = scale
        self.angles = angles

    def angles(self, angles):
        self.angles = angles

    def scale(self, scale):
        self.scale = scale

    def transform(self, coords): #output x, y coord


