import renderer
import numpy as np

class Camera:
    def __init__(self, reach : int, start_settings : list, sensitivity : float):
        self.reach = reach
        self.settings = start_settings # theta, phi, x, y, z
        self.sensitivity = sensitivity
        self.type = 'Camera'

    def rotate(self, rotation : list):
        self.settings[0] += rotation[0] * np.pi / 180 * self.sensitivity
        self.settings[1] += rotation[1] * np.pi / 180 * self.sensitivity
    
    def move(self, displacement : list):
        dis_trans = [displacement[0] * (np.cos(self.settings[0]))  + displacement[1] * np.cos(self.settings[0]),
                                  displacement[0] * (-np.sin(self.settings[0])) + displacement[1] * np.sin(self.settings[0]) ,
                                  displacement[1]
                                 ]
        self.settings[2] += dis_trans[0]
        self.settings[3] += dis_trans[1]
        self.settings[4] += dis_trans[2]
        
    def get_settings(self):
        return self.settings