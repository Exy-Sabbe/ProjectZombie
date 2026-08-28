import pygame
from character import *
from camera import *
from bullet import *


class Player(Character):
    def __init__(self, width, height, speed, map, image_path, corr_angle):
        Character.__init__(self, width, height, speed, map, image_path, corr_angle)
        # Spawn player in the middle of the map
        self._x = (map.GetPixelWidth() - width) / 2
        self._y = (map.GetPixelHeight() - height) / 2

    def HandleUserInputs(self):
        # Get current pressed keys
        keys = pygame.key.get_pressed()

        x = 0
        y = 0

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and not (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            y = -1
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not (keys[pygame.K_UP] or keys[pygame.K_w]):
            y = 1
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            x = -1
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            x = 1

        if (keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
            Bulletmanager().Spawnbullet((self._x, self._y), self.GetForwardsDirection())

        self.SetMoveDirection((x, y))
        self.LookAt(Camera().ConvertToWorldSpace(pygame.mouse.get_pos()))

    def Update(self, delta_time):
        self.HandleUserInputs()
        Character.Update(self, delta_time)