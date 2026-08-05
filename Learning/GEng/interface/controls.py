import Camera
import renderer
import bodies
import pygame as pg
#lock cursor to center of screen

class Controls:
    def __init__(self, camera, bodies):
        self.camera = camera

    def act(self, event):
        if event.type == pg.KEYDOWN:                 # AND DO NOT ALLOW TO CLIP THROUGH OBJECT
            if event.key == pg.K_LEFT:
                self.camera.move([-1, 0, 0])

            if event.key == pg.K_RIGHT:
                self.camera.move([1, 0, 0])

            if event.key == pg.K_UP:
                self.camera.move([0, 1, 0])

            if event.key == pg.K_DOWN:
                self.camera.move([0, -1, 0])

            if event.key == pg.K_SPACE:
            # jump event -- impulse upwards velocity sudden change ONLY IF VERTICAL VELOCITY = 0


        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                # interact with objects - push and create impulse
            if event.button == 3:
                # bring up small menu

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 3:
                # dissapate small menu for object selection

    def init_act(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
            #up through options
            if event.key == pg.K_DOWN:
            #scroll downwards through options
            if event.key == pg.K_SPACE:
            # Select option