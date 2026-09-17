from camera import *
from character import *
import zombiemanager
import mathfunctions as mf

class Zombie(Character):
    def __init__(self, width, height, x_pos, y_pos, speed, health, map, image_path, corr_angle, vision_path, attack_path):
        Character.__init__(self, width, height, x_pos, y_pos, speed, health, map, True, image_path, corr_angle)
        self.__detection_radius = 200
        self.__detection_image = pygame.image.load(vision_path)
        self.__attack_range = 50
        self.__attack_range_image = pygame.image.load(attack_path)
        self.__attack_cooldown = 2
        self.__attack_cooldown_timer = 0
        self.__attack_damage = 20
        self.Init()

    def Init(self):
        return

    def Behavior(self):
        return

    def GetPlayerInVision(self):
        # Get player from zombiemanager, if close enough, return player, otherwise return None
        if mf.IsPositionInRange(self.GetCenterPos(), zombiemanager.ZombieManager().GetPlayer().GetCenterPos(), self.__detection_radius):
            return zombiemanager.ZombieManager().GetPlayer()
        else:
            return None

    def GetAllZombiesInVision(self):
        # Get all zombies, append to list if close enough, return list
        zombies_in_range = []
        for zombie in zombiemanager.ZombieManager().GetZombies():
            if mf.IsPositionInRange(self.GetCenterPos(), zombie.GetCenterPos(), self.__detection_radius):
                zombies_in_range.append(zombie)
        return zombies_in_range

    def __IsPlayerInAttackRange(self):
        return mf.IsPositionInRange(self.GetCenterPos(), zombiemanager.ZombieManager().GetPlayer().GetCenterPos(), self.__attack_range)

    def Update(self, delta_time):
        self.__attack_cooldown_timer -= delta_time
        if self.__IsPlayerInAttackRange():
            if self.__attack_cooldown_timer <= 0:
                self.__attack_cooldown_timer = self.__attack_cooldown
                zombiemanager.ZombieManager().GetPlayer().ModifyHealth(-self.__attack_damage)
        else:
            self.Behavior()
        Character.Update(self, delta_time)

    def Draw(self):
        rect_vision = self.__detection_image.get_rect()
        rect_vision.center = self.GetCenterPos()
        Camera().DrawImageOnWorld(self.__detection_image, rect_vision, DrawLayer.DEBUG)
        rect_attack = self.__attack_range_image.get_rect()
        rect_attack.center = self.GetCenterPos()
        Camera().DrawImageOnWorld(self.__attack_range_image, rect_attack, DrawLayer.DEBUG)
        Camera().DrawRectOnWorld(pygame.Rect(self.GetTopLeftPos()[0] - 1, self.GetTopLeftPos()[1] - 21, self.GetSize() + 2, 12), (0, 0, 0))
        Camera().DrawRectOnWorld(pygame.Rect(self.GetTopLeftPos()[0], self.GetTopLeftPos()[1] - 20, self.GetHealth() / self.GetMaxHealth() * self.GetSize(), 10), mf.GetHealthColor(self.GetHealth(), self.GetMaxHealth()))
        Character.Draw(self)