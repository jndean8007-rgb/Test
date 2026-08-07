import pygame as pg

try:
    from Physics.engine import Engine
    from Physics.world import World
    from interface.controls import Controls
    from interface.renderer import Renderer
except ImportError as error:
    raise ImportError(f"Failed to import game modules: {error}") from error


class Game:
    def __init__(self, width, height, frame_rate, datapath):
        self.width = width
        self.height = height
        self.frame_rate = frame_rate
        self.running = False
        self.mouse_lock = False
        self.dt = 0.0

        pg.init()

        self.world = World(datapath)
        self.world.load()
        self.renderer = Renderer(self.width, self.height, self.world)
        self.controls = Controls(
            self.world.camera[0], self.world.body_list, self.renderer, self
        )
        self.engine = Engine(self.world)
        self.clock = pg.time.Clock()

        self.menu()

    def menu(self):
        tick = 0
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    pg.quit()
                    return
                if self.controls.init_act(event):
                    window_was_closed = self.run()
                    if window_was_closed:
                        return

            self.renderer.initial_screen(tick)
            tick += 1
            self.clock.tick(self.frame_rate)

    def on_off(self):
        self.running = not self.running

    def run(self):
        self.running = True
        self.mouse_lock = True
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        while self.running:
            self.dt = self.clock.tick(self.frame_rate) / 1000

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.world.save()
                    self.running = False
                    pg.quit()
                    return True
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.world.save()
                    self.running = False
                    break
                self.controls.handle_events(event)

            self.controls.handle_held_keys(self.dt)

            if not self.running:
                break

            self.engine.update(self.world, self.dt)
            self.renderer.render()
            if self.mouse_lock:
                self.renderer.mouse_lock()
            pg.display.flip()

        self.mouse_lock = False
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)
        return False

    def get_dt(self):
        return self.dt
