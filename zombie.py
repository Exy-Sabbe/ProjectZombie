from camera import *
from character import *

class Zombie(Character):
    def __init__(self, width, height, x_pos, y_pos, speed, health, map, image_path, corr_angle):
        Character.__init__(self, width, height, x_pos, y_pos, speed, health, map, image_path, corr_angle)
        self.__detection_radius = 200

    def Behavior(self):
        return None

    def Update(self, delta_time):
        self.Behavior()
        Character.Update(self, delta_time)

    def Draw(self):
        Camera().DrawCircleOnWorld(self.GetCenterPos(), self.__detection_radius, (125,125,125,125), DrawLayer.DEBUG)
        Character.Draw(self)