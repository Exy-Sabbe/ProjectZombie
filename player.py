import pygame
import math

# ---- CONSTANTS ----
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 30
PLAYER_SPEED = 5

class Player():
    def __init__(self, window_width, window_height, image_path, corr_angle=0):
        self.window_width = window_width
        self.window_height = window_height
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        self.x = (self.window_width - self.width) / 2
        self.y = (self.window_height - self.height) / 2
        self.half_size = max(self.width, self.height) / 2
        image = pygame.image.load(image_path)
        self.base_image = pygame.transform.scale(image, (self.width, self.height))
        self.image_correction_angle = corr_angle
        self.rot_image = pygame.transform.rotate(self.base_image, 0)
        self.rot_image_rect = None

    def movementBehaviorUser(self):
        # --MOVEMENT--
        # Get current pressed keys
        keys = pygame.key.get_pressed()
        # If keys contains appropriate value, move player in correct direction
        if (keys[pygame.K_UP] or keys[pygame.K_w]):
            self.y = max(self.y - self.speed, self.half_size)
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.y = min(self.y + self.speed, self.window_height - self.half_size)
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.x = max(self.x - self.speed, self.half_size)
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.x = min(self.x + self.speed, self.window_width - self.half_size)

        # --ROTATION--
        # Get angle to rotate image (towards mouse)
        player_rect = self.base_image.get_rect(center = (self.x, self.y))
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - player_rect.centerx, my - player_rect.centery
        angle = math.degrees(math.atan2(-dy, dx)) - self.image_correction_angle

        # Rotate image around center given determined angle
        self.rot_image = pygame.transform.rotate(self.base_image, angle)
        self.rot_image_rect = self.rot_image.get_rect(center = player_rect.center)

    def update(self):
        self.movementBehaviorUser()

    def draw(self, window):
        if self.rot_image_rect is not None:
            window.blit(self.rot_image, self.rot_image_rect.topleft)