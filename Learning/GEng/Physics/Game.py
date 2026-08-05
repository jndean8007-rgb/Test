import pygame as pg
import renderer
import world
import editor
import engine
import camera
import controls
#hide cursor upon game initialization

class Game:
    def __init__(self, width, height, frame_rate, datapath):
        self.width = width
        self.height = height
        self.frame_rate = frame_rate
        self.renderer = renderer.Renderer()
        self.controls = controls.Controls()
        self.editor = editor.Editor()
        self.world = world.World(datapath)
        self.engine = engine.Engine(self.world)
        self.camera = camera.Camera()
        self.running = 'Off'

        pg.init()

        self.clock = pg.time.Clock()
        self.clock.tick(60)

        self.menu()

    def menu(self):
        menu = True
        while menu:
            for event in pg.event.get():
                self.controls.init_act(event)
                self.editor.init_act(event)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        menu = False
                        #destroy pygame window
            self.renderer.initial_screen()
            self.clock.tick(60)

    def on_off(self):
        if self.running == 'Off':
            self.running = 'On'
        else:
            self.running = 'Off'

    def running(self):
        while self.running == 'On':
            for event in pg.event.get():
                self.controls.act(event)
                self.editor.act(event)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = 'Off'
                        self.world.save()
                        self.menu()

            self.engine.update(self.world)
            self.renderer.render(self.width, self.height, self.world.get_bodies())
            self.clock.tick(60)
