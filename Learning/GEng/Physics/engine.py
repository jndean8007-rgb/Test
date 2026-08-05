import world
import collisions
import pygame as pg

class Engine:
    def __init__(self, world):
        self.world = world
        #define world box object

    def update(self, world):

        for force in self.world.force_list: # make all forces act

        #check all collisions to update velocities and forces

        #update all positions with velocities
        for body in self.world.body_list:
            body.velocity
