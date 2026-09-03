import pygame
from character import *
from camera import *
from bullet import *


class Player(Character):
    def HandleUserInputs(self):
        # Get current pressed keys
        keys = pygame.key.get_pressed()

        # Determine move direction based on currect inputs
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

        # Shooting
        if (keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
            Bulletmanager().Spawnbullet(self.GetCenterPos(), self.GetForwardsDirection())

        # Applying movement & rotation to self
        self.SetMoveDirection((x, y))
        self.LookAt(Camera().ConvertToWorldSpace(pygame.mouse.get_pos()))

    def Update(self, delta_time):
        self.HandleUserInputs()
        Character.Update(self, delta_time)