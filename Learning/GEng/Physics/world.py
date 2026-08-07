import json
from pathlib import Path

import numpy as np

try:
    from Physics.bodies import Bodies
    from Physics.forces import Force
    from Physics.World_Setting import World_Setting
    from interface.Camera import Camera
except ImportError as error:
    raise ImportError(f"Failed to import game modules: {error}") from error


class World:
    def __init__(self, datapath):
        self.datapath = datapath
        self.instances = []
        self.body_list = {}
        self.force_list = {}
        self.camera = []
        self.world_setting = None

    def load(self):
        path = Path(self.datapath)
        self.instances = []
        self.body_list.clear()
        self.force_list.clear()
        self.camera.clear()
        self.world_setting = None

        if not path.exists() or path.stat().st_size == 0:
            return

        try:
            with path.open("r", encoding="utf-8") as file:
                loaded = json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"World file '{path}' does not contain valid JSON: {error.msg} "
                f"(line {error.lineno}, column {error.colno})"
            ) from error

        if not isinstance(loaded, list):
            raise ValueError("The world file must contain a JSON list of instances")

        self.instances = loaded
        pending_forces = []

        for item in self.instances:
            if not isinstance(item, dict):
                raise ValueError("Each saved world instance must be a JSON object")

            properties = item.get("properties", item)
            item_type = properties.get("type")
            if item_type is None and isinstance(properties.get("id"), dict):
                item_type = properties["id"].get("type")

            normalized_type = str(item_type).replace(" ", "_").lower()

            if normalized_type == "body":
                body = Bodies(
                    properties["center"],
                    properties["dimensions"],
                    properties["velocity"],
                    properties["mass"],
                    properties["elasticity"],
                    properties["shape"],
                    properties["angles"],
                    None,
                    None,
                    properties["id"],
                )
                self.body_list[body.properties["id"]] = body

            elif normalized_type == "force":
                pending_forces.append(properties)

            elif normalized_type == "camera":
                camera = Camera(
                    properties["reach"],
                    properties["settings"],
                    properties["sensitivity"],
                )
                camera.vz = float(properties.get("vz", 0.0))
                self.camera.append(camera)

            elif normalized_type in {"world_setting", "world_settings"}:
                self.world_setting = World_Setting(
                    properties["dimensions"],
                    properties["shape"],
                    properties['elasticity'],
                )

            else:
                raise ValueError(f"Unknown world instance type: {item_type!r}")

        entities = dict(self.body_list)
        entities.update(
            {
                f"camera:{index}": camera
                for index, camera in enumerate(self.camera)
            }
        )

        for properties in pending_forces:
            entity_id = properties.get("entity_id")
            if entity_id not in entities:
                raise ValueError(
                    f"Force {properties.get('id')!r} refers to unknown entity "
                    f"{entity_id!r}"
                )

            force = Force(
                properties["direction"],
                properties["strength"],
                entities[entity_id],
                None,
                properties["effect"],
                properties["id"],
            )
            self.force_list[force.properties["id"]] = force

        if not self.camera:
            camera = Camera(
                5,
                [0.0,
                0.0,
                1.0,
                1.0,
                0.0],
                0.5,
            )
            camera.vz = 0
            self.camera.append(camera)

    def get_bodies(self):
        return self.body_list

    def get_forces(self):
        return self.force_list

    def get_camera(self):
        return self.camera

    def save(self):
        world_list = []

        for body in self.body_list.values():
            properties = body.properties
            world_list.append(
                {
                    "type": "Body",
                    "id": properties["id"],
                    "center": self._json_value(properties["center"]),
                    "dimensions": self._json_value(properties["dimensions"]),
                    "velocity": self._json_value(properties["velocity"]),
                    "mass": properties["mass"],
                    "elasticity": properties["elasticity"],
                    "shape": self._json_value(properties["shape"]),
                    "angles": self._json_value(properties["angles"]),
                }
            )

        camera_ids = {
            id(camera): f"camera:{index}"
            for index, camera in enumerate(self.camera)
        }
        body_ids = {
            id(body): body.properties["id"]
            for body in self.body_list.values()
        }
        entity_ids = body_ids | camera_ids

        for force in self.force_list.values():
            properties = force.properties
            entity_id = entity_ids.get(id(properties["entity"]))
            if entity_id is None:
                raise ValueError(
                    f"Force {properties['id']!r} is attached to an entity "
                    "that is not stored in this world"
                )
            world_list.append(
                {
                    "type": "Force",
                    "id": properties["id"],
                    "direction": self._json_value(properties["direction"]),
                    "strength": properties["strength"],
                    "effect": properties["effect"],
                    "entity_id": entity_id,
                }
            )

        for camera in self.camera:
            world_list.append(
                {
                    "type": "Camera",
                    "reach": camera.reach,
                    "settings": self._json_value(camera.settings),
                    "sensitivity": camera.sensitivity,
                    "vz": camera.vz,
                }
            )

        if self.world_setting is not None:
            world_list.append(
                {
                    "type": "World_Setting",
                    "dimensions": self._json_value(
                        self.world_setting.properties['dimensions']
                    ),
                    "shape": self._json_value(
                        self.world_setting.properties['shape']
                    ),
                    "elasticity": self._json_value(
                        self.world_setting.properties['elasticity']
                    ),
                }
            )

        path = Path(self.datapath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump(world_list, file, indent=4)

        self.instances = world_list

    @staticmethod
    def _json_value(value):
        if isinstance(value, np.ndarray):
            return value.tolist()
        if isinstance(value, np.generic):
            return value.item()
        if isinstance(value, (list, tuple)):
            return [World._json_value(item) for item in value]
        if isinstance(value, dict):
            return {
                key: World._json_value(item)
                for key, item in value.items()
            }
        return value