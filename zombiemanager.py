import singleton
from zombie import *

class ZombieManager(metaclass=singleton.Singleton):
    def __init__(self, spawn_points, zombie_width, zombie_height, zombie_speed, map, zombie_image_path, zombie_corr_angle):
        self.__zombies = []
        self.__spawn_points = spawn_points
        self.__zombie_width = zombie_width
        self.__zombie_height = zombie_height
        self.__zombie_speed = zombie_speed
        self.__map = map
        self.__zombie_image_path = zombie_image_path
        self.__zombie_corr_angle = zombie_corr_angle
        self.__spawn_cooldown = 3
        self.__spawn_cooldown_timer = 0

    def __SpawnZombies(self):
        for location in self.__spawn_points:
            self.__zombies.append(Zombie(self.__zombie_width, self.__zombie_height, location[0], location[1], self.__zombie_speed, self.__map, self.__zombie_image_path, self.__zombie_corr_angle))

    def Update(self, delta_time):
        for zombie in self.__zombies:
            zombie.Update(delta_time)
        if self.__spawn_cooldown_timer <= 0:
            self.__SpawnZombies()
            self.__spawn_cooldown_timer = self.__spawn_cooldown
        self.__spawn_cooldown_timer -= delta_time

    def Draw(self):
        for zombie in self.__zombies:
            zombie.Draw()