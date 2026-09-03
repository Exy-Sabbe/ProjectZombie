import pygame
from character import *

class Zombie(Character):
    def Zombiebehavior(self):
        self.SetMoveDirection((0, -1))
        self.LookAt((self.GetCenterPos()[0] + 0, self.GetCenterPos()[1] - 1))

    def Update(self, delta_time):
        self.Zombiebehavior()
        Character.Update(self, delta_time)