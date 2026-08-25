import pygame
import camera
from copy import copy
import random

TILE_SIZE = 40
PADDING = 1

class Tile():
    def __init__(self, x_pos, y_pos, size, is_passable = True):
        self.__x = x_pos
        self.__y = y_pos
        self.__size = size
        self.__is_passable = is_passable
        halfsize = self.__size / 2
        self.__rect = pygame.Rect(self.__x - halfsize, self.__y - halfsize, self.__size + PADDING, self.__size + PADDING)

    def GetXPos(self):
        return self.__x

    def GetYPos(self):
        return self.__y

    def GetSize(self):
        return self.__size

    def IsPassable(self):
        return self.__is_passable

    def GetRect(self):
        return self.__rect

    def Draw(self):
        camera.Camera().DrawRectOnWorld(self.__rect, (0, 255, 0) if self.__is_passable else (255, 0, 0))


class Map():
    def __init__(self, width, height, tile_size):
        self.__width = width
        self.__height = height
        self.__tile_size = tile_size
        self.__tiles = []
        for row in range(self.__height):
            for col in range(self.__width):
                passable = True
                if row == 0 or col == 0 or row == self.__height - 1 or col == self.__width - 1:
                    passable = False
                # For now randomize whether a tile is passable or not, will be updated based on map image
                self.__tiles.append(Tile(col * tile_size + tile_size / 2, row * tile_size + tile_size / 2, tile_size, passable))

    def GetTiles(self):
        return self.__tiles

    def GetTileWidth(self):
        return self.__width

    def GetTileHeight(self):
        return self.__height

    def GetPixelWidth(self):
        return self.__width * self.__tile_size

    def GetPixelHeight(self):
        return self.__height * self.__tile_size

    def Draw(self):
        for tile in self.__tiles:
            tile.Draw()