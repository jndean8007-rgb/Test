import pygame as pg
from Physics import World_Setting

class Controls:
    def __init__(self, camera, bodies, renderer, game):
        self.camera = camera
        self.bodies = bodies
        self.renderer = renderer
        self.game = game

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and self.camera.is_on():
                self.camera.vz = 10.0

            elif event.key == pg.K_x:
                for body in self.bodies.values():
                    body.is_x()

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for body in self.bodies.values():
                    body.is_clicked()

                # elif event.button == 3:
                # create random attributes of a body, assign a force
                # catch any possible errors, collisions, overlaps of bodies etc and if good create randomized body

        elif event.type == pg.MOUSEMOTION:
            rel_x, rel_y = event.rel

            dx = rel_x * self.camera.sensitivity
            dy = rel_y * self.camera.sensitivity

            self.camera.rotate([-dx, -dy])

    def handle_held_keys(self, dt):
        keys = pg.key.get_pressed()
        speed = 15.0
        distance = speed * dt

        movement = [0.0, 0.0, 0.0]

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            movement[0] -= distance

        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            movement[0] += distance

        if keys[pg.K_UP] or keys[pg.K_w]:
            movement[1] += distance

        if keys[pg.K_DOWN] or keys[pg.K_s]:
            movement[1] -= distance

        self.camera.move(movement)


    def init_act(self, event):
        if event.type == pg.KEYDOWN:
            #if event.key == pg.K_UP:
            #up through options
            #if event.key == pg.K_DOWN:
            #scroll downwards through options
            if event.key == pg.K_SPACE:
                if self.renderer.init_button == 'is_start_rectangle':
                    self.game.world.world_setting = World_Setting.World_Setting((20, 20, 20), 'rectangle', 0.8)
                    self.game.run()
            # Select option
                #elif init button something else