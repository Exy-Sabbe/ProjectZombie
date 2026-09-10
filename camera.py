import copy
import pygame
import singleton
import math
from enum import Enum

class DrawLayer(Enum):
    MAP = 1,
    DEBUG = 2,
    GAME = 3

class Camera(metaclass=singleton.Singleton):
    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__window = None
        self.__map_surface = None
        self.__debug_surface = None
        self.__game_surface = None
        self.__draw_debug = True

    def SetDrawDebug(self, draw_debug):
        self.__draw_debug = draw_debug

    def SetWindow(self, window):
        self.__window = window
        self.__map_surface = pygame.Surface(window.get_size(), pygame.SRCALPHA)
        self.__debug_surface = pygame.Surface(window.get_size(), pygame.SRCALPHA)
        self.__game_surface = pygame.Surface(window.get_size(), pygame.SRCALPHA)

    def SetCameraPos(self, pos):
        self.__x = pos[0] - self.__window.get_width() / 2
        self.__y = pos[1] - self.__window.get_height() / 2

    def ConvertToWorldSpace(self, pos):
        # Mostly used for mouse position
        world_pos = (pos[0] + self.__x, pos[1] + self.__y)
        return world_pos

    def ClearAllSurfaces(self):
        self.__map_surface = pygame.Surface(self.__window.get_size(), pygame.SRCALPHA)
        self.__debug_surface = pygame.Surface(self.__window.get_size(), pygame.SRCALPHA)
        self.__game_surface = pygame.Surface(self.__window.get_size(), pygame.SRCALPHA)

    def Draw(self):
        self.__window.blit(self.__map_surface, (0, 0))
        if self.__draw_debug:
            self.__window.blit(self.__debug_surface, (0, 0))
        self.__window.blit(self.__game_surface, (0, 0))

    def DrawRectOnWorld(self, rect, color, layer = DrawLayer.GAME):
        # Apply negative camera position to anything being drawn
        camera_rect = copy.copy(rect)
        camera_rect.x -= self.__x
        camera_rect.y -= self.__y

        if layer == DrawLayer.MAP:
            pygame.draw.rect(self.__map_surface, color, camera_rect)
        elif layer == DrawLayer.DEBUG:
            pygame.draw.rect(self.__debug_surface, color, camera_rect)
        elif layer == DrawLayer.GAME:
            pygame.draw.rect(self.__game_surface, color, camera_rect)

    def DrawCircleOnWorld(self, center, radius, color, layer = DrawLayer.GAME):
        # Apply negative camera position to anything being drawn
        camera_center = (center[0] - self.__x, center[1] - self.__y)

        if layer == DrawLayer.MAP:
            pygame.draw.circle(self.__map_surface, color, camera_center, radius)
        elif layer == DrawLayer.DEBUG:
            pygame.draw.circle(self.__debug_surface, color, camera_center, radius)
        elif layer == DrawLayer.GAME:
            pygame.draw.circle(self.__game_surface, color, camera_center, radius)

    def DrawArcOnWorld(self, center, radius, color, layer = DrawLayer.GAME):
        arc_rect = pygame.Rect(center[0] - radius, center[1] - radius, radius * 2, radius * 2)
        arc_rect.x -= self.__x
        arc_rect.y -= self.__y
        if layer == DrawLayer.MAP:
            pygame.draw.arc(self.__map_surface, color, arc_rect, 0, math.pi * 2)
        elif layer == DrawLayer.DEBUG:
            pygame.draw.arc(self.__debug_surface, color, arc_rect, 0, math.pi * 2)
        elif layer == DrawLayer.GAME:
            pygame.draw.arc(self.__game_surface, color, arc_rect, 0, math.pi * 2)

    def DrawImageOnWorld(self, image, image_rect, layer = DrawLayer.GAME):
        # Apply negative camera position to anything being drawn
        image_pos = (image_rect.topleft[0] - self.__x, image_rect.topleft[1] - self.__y)
        if layer == DrawLayer.MAP:
            self.__map_surface.blit(image, image_pos)
        elif layer == DrawLayer.DEBUG:
            self.__debug_surface.blit(image, image_pos)
        elif layer == DrawLayer.GAME:
            self.__game_surface.blit(image, image_pos)