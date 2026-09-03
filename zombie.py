import pygame
import random
import math
from character import *

class Zombie(Character):
    def __init__(self, width, height, x_pos, y_pos, speed, health, map, image_path, corr_angle):
        Character.__init__(self, width, height, x_pos, y_pos, speed, health, map, image_path, corr_angle,)
        self.__angle = random.randint(1, 360)

    def Zombiebehavior(self):
        dir = (math.cos(math.radians(self.__angle)), math.sin(math.radians(self.__angle)))
        self.__angle += random.randint(-10, 10) / 10
        self.SetMoveDirection(dir)
        self.LookAt((self.GetCenterPos()[0] + dir[0], self.GetCenterPos()[1] - dir[1]))

    def Update(self, delta_time):
        self.Zombiebehavior()
        Character.Update(self, delta_time)