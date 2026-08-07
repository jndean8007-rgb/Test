from Physics import world
import numpy as np


class Force:
    def __init__(self, direction, strength: float, entity, game, effect, id):
        self.properties = {
            "direction": np.asarray(direction, dtype=float),
            "strength": float(strength),
            "entity": entity,
            "type": "Force",
            "effect": effect,
            "id": id,
        }

    def act(self, dt: float):
        if self.properties["effect"] != "gravity":
            return

        entity = self.properties["entity"]
        direction = self.properties["direction"]
        acceleration = direction * self.properties["strength"]

        if hasattr(entity, "vz"):
            if not entity.is_on():
                entity.vz += acceleration[2] * dt
            return

        if hasattr(entity, "properties") and "velocity" in entity.properties:
            entity.properties["velocity"] += acceleration * dt
        #elif

    #def air resistance





