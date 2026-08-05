#store all objects, forces, collisions
# add id options
# add hardness per object
import json
import bodies
import forces
import Camera
import World_Setting
import os

class World:
    def __init__(self, datapath):
        #adquire json data for each object and world details
        self.datapath = datapath
        self.instances = []
        self.body_list = {}
        self.force_list = {}
        self.camera = []
        self.world_setting = []

    def load(self):
        #turn json data into objects, forces, camera, borders etc
        try:
            if not os.path.exists(self.datapath):
                print(f"Error: File '{self.datapath}' does not exist.")
                return None

            with open(f"{self.datapath}", "r", encoding = "utf-8") as file:
                self.instances = json.load(file)
            for item in self.instances:
                if item.type == 'Body':
                    self.body_list[item[8]] = (bodies.Bodies(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8]))
                elif item.type == 'Force':
                    self.force_list[item[5]] = (forces.Force(item[0], item[1], item[2], item[3], item[4], item[5]))
                elif item.type == 'Camera':
                    self.camera.append(Camera.Camera(item[0], item[1], item[2]))
                elif item.type == 'World Setting':
                    self.world_setting.append(World_Setting.World_Setting(item[0]))

        except FileNotFoundError:
            print(f"Error: File '{self.datapath}' not found.")

    def get_bodies(self):
        return self.body_list

    def get_forces(self):
        return self.force_list

    def get_camera(self):
        return self.camera

    def save(self):
        #write state of all things into json file
        # turn dictionaries into lists describing stats
        self.world_list = # join self.body_list + self.force_list + self.camera -- append camera type + self.world_setting -- append world_setting type
        try:
            if not os.path.exists(self.datapath):
                print(f"Error: File '{self.datapath}' does not exist.")
                return None

            with open(f"{self.datapath}", "w", encoding = "utf-8") as file:
                json.dump(self.world_list, file, indent = 4)

        except FileNotFoundError:
            print(f"Error: File '{self.datapath}' not found.")
