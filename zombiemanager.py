import singleton
import random
from zombie import *

class ZombieManager(metaclass=singleton.Singleton):
    def __init__(self, spawn_points, zombie_width, zombie_height, zombie_speed, zombie_health, map, zombie_image_path, zombie_corr_angle, start_amount, increment, timer):
        self.__zombies = []
        self.__spawn_points = spawn_points
        self.__zombie_width = zombie_width
        self.__zombie_height = zombie_height
        self.__zombie_speed = zombie_speed
        self.__zombie_health = zombie_health
        self.__map = map
        self.__zombie_image_path = zombie_image_path
        self.__zombie_corr_angle = zombie_corr_angle
        self.__requested_zombies = start_amount
        self.__increment_zombies = increment
        self.__increment_timer = timer
        self.__increment_timer_value = 0

    def __GetRandomSpawnPoint(self):
        return self.__spawn_points[random.randint(0, len(self.__spawn_points) - 1)]

    def GetZombies(self):
        return self.__zombies

    def Update(self, delta_time):
        # Remove all dead zombies
        temp_zombies = []
        for zombie in self.__zombies:
            if zombie.GetHealth() > 0:
                temp_zombies.append(zombie)
        self.__zombies = temp_zombies

        # Slowly increment amount of wanted zombies
        self.__increment_timer_value += delta_time
        if self.__increment_timer_value > self.__increment_timer:
            self.__requested_zombies += self.__increment_zombies
            self.__increment_timer_value = 0

        # Spawn more zombies until requested amount is reached
        while len(self.__zombies) <= self.__requested_zombies:
            spawn_location = self.__GetRandomSpawnPoint()
            self.__zombies.append(Zombie(self.__zombie_width, self.__zombie_height, spawn_location[0], spawn_location[1], self.__zombie_speed, self.__zombie_health, self.__map, self.__zombie_image_path, self.__zombie_corr_angle))

        # Update existing zombies
        for zombie in self.__zombies:
            zombie.Update(delta_time)

    def Draw(self):
        for zombie in self.__zombies:
            zombie.Draw()