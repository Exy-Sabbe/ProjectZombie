import singleton
import pygame
import camera
import math

class Bullet():
    def __init__(self, position, speed, direction, image, correction_angle):
        self.__speed = speed
        # Normalize direction just in case
        length = math.sqrt(direction[0]**2 + direction[1]**2)
        self.__direction = (direction[0] / length, direction[1] / length)
        # Rotate bullet image towards direction
        self.__image = pygame.transform.rotate(image, math.degrees(math.atan2(-direction[1], direction[0])) - correction_angle)
        self.__image_rect = self.__image.get_rect(center = (position))
        self.__lifetime = 0

    def GetLifeTime(self):
        return self.__lifetime

    def IsOverlappingWithWall(self, map):
        for tile in map.GetTiles():
            if not tile.IsPassable() and self.__image_rect.colliderect(tile.GetRect()):
                return True
        return False

    def Update(self, delta_time):
        speed = self.__speed * delta_time
        self.__image_rect.x += self.__direction[0] * speed
        self.__image_rect.y += self.__direction[1] * speed
        self.__lifetime += delta_time

    def Draw(self):
        camera.Camera().DrawImageOnWorld(self.__image, self.__image_rect)

class Bulletmanager(metaclass=singleton.Singleton):
    def __init__(self, bullet_image_path, bullet_corr_angle, bullet_speed, bullet_lifetime, bullet_cooldown, map):
        self.__bullet_image = pygame.image.load(bullet_image_path)
        self.__bullet_correction_angle= bullet_corr_angle
        self.__bullet_speed = bullet_speed
        self.__bullet_max_lifetime = bullet_lifetime
        self.__bullets = []
        self.__bullet_cooldown = bullet_cooldown
        self.__bullet_timer = 0
        self.__map = map

    def Spawnbullet(self, position, direction):
        # If bullet cooldown allows it, spawns bullet in position with direction
        if self.__bullet_timer <= 0:
            self.__bullets.append(Bullet(position, self.__bullet_speed, direction, self.__bullet_image, self.__bullet_correction_angle))
            self.__bullet_timer = self.__bullet_cooldown

    def Update(self, delta_time):
        new_bullets = []
        for bullet in self.__bullets:
            # Move bullet
            bullet.Update(delta_time)
            # If bullet hits wall OR exists for longer than max_lifetime, destroy it
            if bullet.GetLifeTime() < self.__bullet_max_lifetime and not bullet.IsOverlappingWithWall(self.__map):
                new_bullets.append(bullet)
        self.__bullets = new_bullets
        # Update bullet cooldown timer
        self.__bullet_timer -= delta_time

    def Draw(self):
        for bullet in self.__bullets:
            bullet.Draw()