
class World_Setting:
    def __init__(self, dimensions): #much later add different types of world such as sphere etc and perhaps more complicated settings
        self.vertices = [[0,0,0], [dimensions[0], 0, 0],
                         [0, dimensions[0], 0], [dimensions[0], dimensions[0], 0],
                         [0, 0, dimensions[0]], [dimensions[0], 0, dimensions[0]],
                         [0, dimensions[0], dimensions[0]], [dimensions[0], dimensions[0], dimensions[0]]
                         ]
        self.type = 'World_Settings'