import pygame
import random

TILE_SIZE = 40

class Tile():
    def __init__(self, position_x, position_y, size, is_passable = True):
        self.position_x = position_x
        self.position_y = position_y
        self.size = size
        self.is_passable = is_passable
        halfsize = self.size / 2
        self.rect = pygame.Rect(self.position_x - halfsize, self.position_y - halfsize, self.size, self.size)

    def draw(self, window):
        # For now draw a Green/Red rectangle to see if it is passable or not, images to be added later
        pygame.draw.rect(window, (0, 255, 0) if self.is_passable else (255, 0, 0), self.rect)


class Map():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_size = TILE_SIZE
        self.tiles = []
        for row in range(self.height):
            for col in range(self.width):
                # For now randomize whether a tile is passable or not, will be updated based on map image
                self.tiles.append(Tile(col * self.tile_size + self.tile_size / 2, row * self.tile_size + self.tile_size / 2, self.tile_size, bool(random.getrandbits(4))))

    def draw(self, window):
        for tile in self.tiles:
            tile.draw(window)