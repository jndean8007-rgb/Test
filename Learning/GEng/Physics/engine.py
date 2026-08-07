from itertools import combinations

try:
    from Physics.collisions import Collisions
except ImportError as error:
    raise ImportError(f"Failed to import game modules: {error}") from error

class Engine:
    def __init__(self, world):
        self.world = world

    def update(self, world=None, dt=0.0):
        if world is not None:
            self.world = world

        for force in self.world.force_list.values():
            force.act(dt)

        for body in self.world.body_list.values():
            body.properties["center"] += body.properties["velocity"] * dt

        objects = list(self.world.body_list.values())
        Collisions.check_collisions(combinations(objects, 2))
        for body in objects:
            Collisions.collide_with_world(
                body,
                self.world.world_setting,
            )

        explicitly_forced_entities = {
            id(force.properties["entity"])
            for force in self.world.force_list.values()
        }

        for camera in self.world.camera:
            if id(camera) not in explicitly_forced_entities:
                camera.force.act(dt)
            camera.integrate(dt)