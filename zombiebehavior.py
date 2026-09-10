import random
from zombie import *


class ZombieBehavior(Zombie):
    def __init__(self, width, height, x_pos, y_pos, speed, health, map, image_path, corr_angle, vision_path, vision_corr_angle):
        Zombie.__init__(self, width, height, x_pos, y_pos, speed, health, map, image_path, corr_angle, vision_path, vision_corr_angle)
        self.__angle = random.randint(1, 360)
        self.__map_center = (map.GetPixelWidth() / 2, map.GetPixelHeight() / 2)

    def Behavior(self):
        self.WanderBehavior()

    def WanderBehavior(self):
        random_dir = (math.cos(math.radians(self.__angle)), math.sin(math.radians(self.__angle)))
        self.__angle += random.randint(-10, 10) / 10
        pull_to_center_dir = (self.__map_center[0] - self.GetCenterPos()[0], self.__map_center[1] - self.GetCenterPos()[1])
        length_pull = math.sqrt(pull_to_center_dir[0]**2 + pull_to_center_dir[1]**2)
        pull_to_center_dir = (pull_to_center_dir[0] / length_pull, pull_to_center_dir[1] / length_pull)
        final_dir = (random_dir[0] + pull_to_center_dir[0] * 0.2, random_dir[1] + pull_to_center_dir[1] * 0.2)
        self.SetMoveDirection(final_dir)
        self.LookAt((self.GetCenterPos()[0] + final_dir[0], self.GetCenterPos()[1] - final_dir[1]))