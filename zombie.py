import pygame
import camera
import math
from character import *

class Zombie(Character):
    def __init__(self, width, height, x_pos, y_pos, speed, health, map, image_path, corr_angle, vision_path, vision_corr_angle):
        Character.__init__(self, width, height, x_pos, y_pos, speed, health, map, image_path, corr_angle)
        image = pygame.image.load(vision_path)
        self.__vision_image = pygame.transform.scale(image, (width * 8, height * 8))
        self.__vision_correction_angle = vision_corr_angle
        self.__rot_vision = pygame.transform.rotate(self.__vision_image, 0)
        self.__rot_vision_rect = None

    def Behavior(self):
        return None

    def Update(self, delta_time):        
        # Rotate image around center given determined angle
        self.__rot_vision = pygame.transform.rotate(self.__vision_image, self.GetRotAngle())
        self.__rot_vision_rect = self.__rot_vision.get_rect(center = self.GetCenterPos())
        self.Behavior()
        Character.Update(self, delta_time)

    def Draw(self):
        camera.Camera().DrawImageOnWorld(self.__rot_vision, self.__rot_vision_rect, True)
        Character.Draw(self)