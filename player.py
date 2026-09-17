import pygame
from character import Character
from camera import Camera
from bullet import BulletManager
import mathfunctions as mf

class Player(Character):
    def __init__(self, width, height, x_pos, y_pos, speed, health, map, should_look_forward, image_path, corr_angle, is_ai):
        Character.__init__(self, width, height, x_pos, y_pos, speed, health, map, should_look_forward, image_path, corr_angle)
        self.__is_ai = is_ai
        self.Init()

    def Init(self):
        return
    
    def __HandleUserInputs(self):
        # Get current pressed keys
        keys = pygame.key.get_pressed()

        # Determine move direction based on currect inputs
        x = 0
        y = 0
        if (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_z]) and not (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            y = -1
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not (keys[pygame.K_UP] or keys[pygame.K_w] or keys[pygame.K_z]):
            y = 1
        if (keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_q]) and not (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            x = -1
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not (keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_q]):
            x = 1

        # Shooting
        if (keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]):
            BulletManager().Spawnbullet(self.GetCenterPos(), self.GetForwardsDirection())

        # Applying movement & rotation to self
        self.SetMoveDirection((x, y))
        self.LookAt(Camera().ConvertToWorldSpace(pygame.mouse.get_pos()))

    def Behavior(self):
        return

    def Update(self, delta_time):
        if self.__is_ai:
            self.Behavior()
        else:
            self.__HandleUserInputs()
        Character.Update(self, delta_time)

    def Draw(self):
        Camera().DrawRectOnScreen((47, pygame.display.get_window_size()[1] - 78, 106, 31), ((0, 0, 0)))
        Camera().DrawRectOnScreen((50, pygame.display.get_window_size()[1] - 75, self.GetHealth() / self.GetMaxHealth() * 100, 25), mf.GetHealthColor(self.GetHealth(), self.GetMaxHealth()))
        Character.Draw(self)