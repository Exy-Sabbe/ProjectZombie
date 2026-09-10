from camera import *
from character import *
import zombiemanager

class Zombie(Character):
    def __init__(self, width, height, x_pos, y_pos, speed, health, map, image_path, corr_angle, vision_path):
        Character.__init__(self, width, height, x_pos, y_pos, speed, health, map, True, image_path, corr_angle)
        self.__detection_radius = 200
        self.__detection_image = pygame.image.load(vision_path)

    def Behavior(self):
        return None

    def GetPlayerInRange(self):
        player_pos = zombiemanager.ZombieManager().GetPlayer().GetCenterPos()
        zombie_pos = self.GetCenterPos()
        if (player_pos[0] - zombie_pos[0])**2 + (player_pos[1] - zombie_pos[1])**2 <= self.__detection_radius**2:
            return zombiemanager.ZombieManager().GetPlayer()
        else:
            return None

    def GetAllZombiesInRange(self):
        zombies_in_range = []
        for zombie in zombiemanager.ZombieManager().GetZombies():
            zombie_pos = zombie.GetCenterPos()
            own_pos = self.GetCenterPos()
            if (zombie_pos[0] - own_pos[0])**2 + (zombie_pos[1] - own_pos[1])**2 <= self.__detection_radius**2:
                zombies_in_range.append(zombie)
        return zombies_in_range

    def Update(self, delta_time):
        self.Behavior()
        Character.Update(self, delta_time)

    def Draw(self):
        rect = self.__detection_image.get_rect()
        rect.center = self.GetCenterPos()
        Camera().DrawImageOnWorld(self.__detection_image, rect, DrawLayer.DEBUG)
        Camera().DrawArcOnWorld(self.GetCenterPos(), self.__detection_radius, (0, 0, 0), DrawLayer.DEBUG)
        Character.Draw(self)