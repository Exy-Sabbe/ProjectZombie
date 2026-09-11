import copy
import pygame
import singleton
import math
from enum import Enum

# Used to ensure draw order, THEY GET DRAWN IN THE ORDER PUT HERE
class DrawLayer(Enum):
    MAP = 0,
    DEBUG = 1,
    GAME = 2

class Camera(metaclass=singleton.Singleton):
    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__window = None
        self.__surfaces = {}
        self.__draw_debug = True

    # Determine if Debug layer should be drawn
    def SetDrawDebug(self, draw_debug):
        self.__draw_debug = draw_debug

    def SetWindow(self, window):
        # Set window variable (to prevent __init__ taking vars for singleton), init surfaces based on amount of drawlayers
        self.__window = window
        for layer in DrawLayer:
            self.__surfaces[layer] = pygame.Surface(window.get_size(), pygame.SRCALPHA)

    def SetCameraPos(self, pos):
        self.__x = pos[0] - self.__window.get_width() / 2
        self.__y = pos[1] - self.__window.get_height() / 2

    def ConvertToWorldSpace(self, pos):
        # Mostly used for mouse position
        world_pos = (pos[0] + self.__x, pos[1] + self.__y)
        return world_pos

    def ClearAllSurfaces(self):
        for layer in DrawLayer:
            self.__surfaces[layer] = pygame.Surface(self.__window.get_size(), pygame.SRCALPHA)

    def Draw(self):
        for layer in DrawLayer:
            # Dont draw debug layer if debug is set to false
            if layer == DrawLayer.DEBUG and not self.__draw_debug:
                continue
            self.__window.blit(self.__surfaces[layer], (0, 0))

    def DrawRectOnWorld(self, rect, color, layer = DrawLayer.GAME):
        # Apply negative camera position to anything being drawn
        camera_rect = copy.copy(rect)
        camera_rect.x -= self.__x
        camera_rect.y -= self.__y
        # Draw on correct surface
        pygame.draw.rect(self.__surfaces[layer], color, camera_rect)

    def DrawCircleOnWorld(self, center, radius, color, layer = DrawLayer.GAME):
        # Apply negative camera position to anything being drawn
        camera_center = (center[0] - self.__x, center[1] - self.__y)
        # Draw on correct surface
        pygame.draw.circle(self.__surfaces[layer], color, camera_center, radius)

    def DrawArcOnWorld(self, center, radius, color, layer = DrawLayer.GAME):
        # Apply negative camera position to anything being drawn
        arc_rect = pygame.Rect(center[0] - radius, center[1] - radius, radius * 2, radius * 2)
        arc_rect.x -= self.__x
        arc_rect.y -= self.__y
        # Draw on correct surface
        pygame.draw.arc(self.__surfaces[layer], color, arc_rect, 0, math.pi * 2)

    def DrawImageOnWorld(self, image, image_rect, layer = DrawLayer.GAME):
        # Apply negative camera position to anything being drawn
        image_pos = (image_rect.topleft[0] - self.__x, image_rect.topleft[1] - self.__y)
        # Draw on correct surface
        self.__surfaces[layer].blit(image, image_pos)