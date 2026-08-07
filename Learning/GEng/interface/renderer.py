import numpy as np
import pygame as pg

try:
    from interface.Camera import Camera
except ImportError as error:
    raise ImportError(f"Failed to import game modules: {error}") from error


class Renderer:
    def __init__(self, width, height, world):
        self.world = world
        if not self.world.camera:
            self.world.camera.append(Camera(5, [0, 0, 1, 1, 1], 1))

        self.properties = {
            "width": int(width),
            "height": int(height),
            "camera": self.world.camera[0],
        }
        self.window = pg.display.set_mode(
            (self.properties["width"], self.properties["height"])
        )
        pg.font.init()
        self.font = pg.font.SysFont(None, 36)
        pg.display.set_caption("The World")
        self.init_button = "is_start_rectangle"

    def initial_screen(self, tick):
        self.init_button = "is_start_rectangle"
        self.window.fill((0, 0, 0))
        start_button = pg.Rect(
            self.properties["width"] // 2 - 100,
            self.properties["height"] // 2 - 80,
            200,
            50,
        )

        if (tick // 30) % 2 == 0:
            pg.draw.rect(self.window, (0, 200, 0), start_button, 2)

        text = self.font.render("Space, rectangle", True, (255, 255, 255))
        self.window.blit(
            text,
            (
                start_button.centerx - text.get_width() // 2,
                start_button.centery - text.get_height() // 2,
            ),
        )
        pg.display.flip()

    def mouse_lock(self):
        center = (
            self.properties["width"] // 2,
            self.properties["height"] // 2,
        )
        pg.mouse.set_pos(center)
        pg.draw.line(
            self.window,
            (255, 0, 0),
            (center[0] - 10, center[1]),
            (center[0] + 10, center[1]),
            2,
        )
        pg.draw.line(
            self.window,
            (255, 0, 0),
            (center[0], center[1] - 10),
            (center[0], center[1] + 10),
            2,
        )

    def render(self):
        self.window.fill((0, 0, 0))

        if self.world.world_setting is not None:
            self.draw_item_3d(self.world.world_setting)

        for item in self.world.body_list.values():
            self.draw_item_3d(item)

    def transform(self, coordinates):
        theta, phi, camera_x, camera_y, camera_z = (
            self.properties["camera"].get_settings()
        )
        relative = np.asarray(coordinates, dtype=float) - np.array(
            [camera_x, camera_y, camera_z], dtype=float
        )

        right = np.array([np.cos(theta), np.sin(theta), 0.0])
        forward = np.array(
            [-np.sin(theta) * np.cos(phi),
             np.cos(theta) * np.cos(phi),
             np.sin(phi)]
        )
        up = np.cross(right, forward)

        view_x = np.dot(relative, right)
        view_y = np.dot(relative, up)
        depth = np.dot(relative, forward)

        if depth <= 0.01:
            return None

        focal_length = min(
            self.properties["width"], self.properties["height"]
        ) / 2
        screen_x = self.properties["width"] / 2 + focal_length * view_x / depth
        screen_y = self.properties["height"] / 2 - focal_length * view_y / depth
        return round(screen_x), round(screen_y)

    def draw_item_3d(self, item):
        item_type = getattr(item, "type", item.properties.get("type"))
        if item_type == "World_Settings":
            for a, b in item.edges:
                start = self.transform(item.vertices[a])
                end = self.transform(item.vertices[b])
                if start is not None and end is not None:
                    pg.draw.line(self.window, (255, 255, 255), start, end, 2)
        if item_type =='Body':
            if item.properties['shape'] == 'rectangle' or item.properties['shape'] == 'tetrahedron':
                for a, b in item.edges:
                    start = self.transform(item.world_vertices[a])
                    end = self.transform(item.world_vertices[b])
                    if start is not None and end is not None:
                        pg.draw.line(self.window, (255, 255, 255), start, end, 2)

            if item.properties['shape'] == 'sphere':
                relative_position = (
                        item.properties["center"] - self.world.camera.position
                )

                depth = np.dot(relative_position, self.world.camera.forward)

                if depth > 0:
                    focal_length = min(
                        self.properties["width"], self.properties["height"]
                    ) / 2

                    screen_radius = max(
                        1,
                        int(item.radius * focal_length / depth),
                    )

                    transformed = self.transform(item.properties["center"])

                    if transformed is not None:
                        screen_x = int(np.asarray(transformed[0]))
                        screen_y = int(np.asarray(transformed[1]))

                        screen_center = (screen_x, screen_y)

                        pg.draw.circle(
                            self.window,
                            (255, 255, 255),
                            screen_center,
                            screen_radius,
                        )