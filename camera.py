import copy
import pygame
import singleton

class Camera(metaclass=singleton.Singleton):
    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__window = None

    def SetWindow(self, window):
        self.__window = window

    def SetCameraPos(self, pos):
        self.__x = pos[0] - self.__window.get_width() / 2
        self.__y = pos[1] - self.__window.get_height() / 2

    def ConvertToWorldSpace(self, pos):
        world_pos = (pos[0] + self.__x, pos[1] + self.__y)
        return world_pos

    def DrawRectOnWorld(self, rect, color):
        camera_rect = copy.copy(rect)
        camera_rect.x -= self.__x
        camera_rect.y -= self.__y
        pygame.draw.rect(self.__window, color, camera_rect)

    def DrawImageOnWorld(self, image, image_rect):
        image_pos = (image_rect.topleft[0] - self.__x, image_rect.topleft[1] - self.__y)
        self.__window.blit(image, image_pos)