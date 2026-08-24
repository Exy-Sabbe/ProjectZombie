import pygame
import character
import camera

class Player(character.Character):
    def __init__(self, width, height, speed, map, image_path, corr_angle=0):
        character.Character.__init__(self, width, height, speed, map, image_path, corr_angle)
        # Spawn player in the middle of the map
        self._x = (map.GetPixelWidth() - width) / 2
        self._y = (map.GetPixelHeight() - height) / 2

    def HandleUserInputs(self):
        # Get current pressed keys
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_UP] or keys[pygame.K_w]):
            self.MoveUp()
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.MoveDown()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.MoveLeft()
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.MoveRight()


        look_position = pygame.mouse.get_pos()
        look_position = (look_position[0] + camera.Camera().GetXPos(), look_position[1] + camera.Camera().GetYPos())
        self.LookAt(look_position)

    def Update(self, delta_time):
        self.HandleUserInputs()
        character.Character.Update(self, delta_time)