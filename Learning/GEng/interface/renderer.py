import pygame as pg
import Camera
import world

class Renderer:
    def __init__(self, width, height, camera, world):
        self.properties = {'width' : width, 'height' : height, 'camera' : camera}
        self.world = world
        self.window = pg.display.set_mode((self.properties['width'], self.properties['height']))
        pg.display.set_caption("The World")

    def initial_screen(self):
    """
    green flashing button when selected

    """

    def render(self):
        self.draw_item_3d(self.world.world_setting)

        for item  in self.world.body_list:
            self.draw_item_3d(item)

    def transform(self, coordinates):
        cam_now = self.properties['camera'].get_settings[1:6]

        #called by draw_item_3d



    def draw_item_3d(self, item):
        self.window.fill((0, 0, 0))
        if item.type == 'World_Setting':
            pg.draw_line(self.window, (255, 255, 255),
                         self.transform(self.world.verticies[0])[0], self.transform(self.world.verticies[0])[1],
                         self.transform(self.world.verticies[1])[0], self.transform(self.world.verticies[1])[1], 2)
            """
            0–1
            0–2
            0–4
            1–3
            1–5
            2–3
            2–6
            3–7
            4–5
            4–6
            5–7
            6–7
            """
        elif item.type == 'Sphere':

        elif item.type == 'Rectangle':

        #elif item.type == ''