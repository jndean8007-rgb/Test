import world
import Game
# add angle torque etc

class Force:
    def __init__(self, direction, strength, entity, game, effect, id):
        self.properties = {'Direction': direction,
                                               'Strength': strength,
                                               'entity' : entity,
                                               'game' : game,
                                               'type' : 'Force',
                                               'effect' : effect,
                                               'id' : id}


    def gravity(self):
        #check if on top of other object or on ground
        self.properties['entity'].velocity += self.properties['direction'] * self.properties['strength'] * self.['game'].clock.tick(60) / 1000

    #def air resistance





