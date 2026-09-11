import random
from zombie import *

class ZombieBehavior(Zombie):
    # Initialize desired variables
    def Init(self):
        self.__angle = random.randint(1, 360)

    # Define Zombie behavior
    def Behavior(self):
        player = self.GetPlayerInRange()
        if player is None:
            self.WanderBehavior()
        else:
            dir = (player.GetCenterPos()[0] - self.GetCenterPos()[0], player.GetCenterPos()[1] - self.GetCenterPos()[1])
            self.SetMoveDirection(dir)
            self.__angle = -self.GetRotAngle()

    def WanderBehavior(self):
        self.__angle += random.randint(-10, 10) / 10
        random_dir = (math.cos(math.radians(self.__angle)), math.sin(math.radians(self.__angle)))
        self.SetMoveDirection(random_dir)
        self.LookAt((self.GetCenterPos()[0] + random_dir[0] * 2, self.GetCenterPos()[1] + random_dir[1] * 2))