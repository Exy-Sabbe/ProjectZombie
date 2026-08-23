import pygame
import math
import map

# ---- CONSTANTS ----
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 30
PLAYER_SPEED = 0.5

class Player():
    def __init__(self, map, image_path, corr_angle=0):
        self.game_width = map.width * map.tile_size
        self.game_height = map.height * map.tile_size
        self.map = map
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.speed = PLAYER_SPEED
        # Spawn player in the middle of the map
        self.x = (self.game_width - self.width) / 2
        self.y = (self.game_height - self.height) / 2
        self.half_size = max(self.width, self.height) / 2
        image = pygame.image.load(image_path)
        self.base_image = pygame.transform.scale(image, (self.width, self.height))
        self.image_correction_angle = corr_angle
        self.rot_image = pygame.transform.rotate(self.base_image, 0)
        self.rot_image_rect = None

    def movementBehaviorUser(self, delta_time):
        # --MOVEMENT--
        # Get current pressed keys
        keys = pygame.key.get_pressed()

        # Make speed independant on framerate
        speed = self.speed * delta_time

        # Determine new temporary position of player (if correct keys are pressed)
        potential_new_x = None
        potential_new_y = None

        if (keys[pygame.K_UP] or keys[pygame.K_w]):
            potential_new_y = max(self.y - speed, self.half_size)
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            potential_new_y = min(self.y + speed, self.game_height - self.half_size)
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            potential_new_x = max(self.x - speed, self.half_size)
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            potential_new_x = min(self.x + speed, self.game_width - self.half_size)

        # If player moved, check if the new position overlaps with an impassable tile and correct
        if potential_new_x is not None or potential_new_y is not None:    
            self.x, self.y = self.calculateClippedPos(self.x if potential_new_x is None else potential_new_x, self.y if potential_new_y is None else potential_new_y)

        # --ROTATION--
        # Get angle to rotate image (towards mouse)
        player_rect = self.base_image.get_rect(center = (self.x, self.y))
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - player_rect.centerx, my - player_rect.centery
        angle = math.degrees(math.atan2(-dy, dx)) - self.image_correction_angle

        # Rotate image around center given determined angle
        self.rot_image = pygame.transform.rotate(self.base_image, angle)
        self.rot_image_rect = self.rot_image.get_rect(center = player_rect.center)

    def calculateClippedXPos(self, tile, x_pos):
        if tile.position_x + tile.size / 2 > x_pos - self.half_size and tile.position_x < x_pos:
            return tile.position_x + tile.size / 2 + self.half_size
        elif tile.position_x - tile.size / 2 < x_pos + self.half_size and tile.position_x > x_pos:
            return tile.position_x - tile.size / 2 - self.half_size
        # Can't normally happen because we already confirmed tile is overlapping in calculateClippedPos
        return x_pos

    def calculateClippedYPos(self, tile, y_pos):
        if tile.position_y + tile.size / 2 > y_pos - self.half_size and tile.position_y < y_pos:
            return tile.position_y + tile.size / 2 + self.half_size
        elif tile.position_y - tile.size / 2 < y_pos + self.half_size and tile.position_y > y_pos:
            return tile.position_y - tile.size / 2 - self.half_size
        # Can't normally happen because we already confirmed tile is overlapping in calculateClippedPos
        return y_pos

    def calculateClippedPos(self, x_pos, y_pos):
        # Create temporary rect with given position to check if it overlaps with any tiles tile
        rect = pygame.Rect(x_pos - self.half_size, y_pos - self.half_size, max(self.width, self.height), max(self.width, self.height))

        # Check all tiles
        for tile in self.map.tiles:
            if tile.is_passable:
                continue
            
            # If temp rect overlaps with tile, correct either X or Y pos (depending on which overlap is bigger)
            if rect.colliderect(tile.rect):
                if abs(tile.position_x - self.x) > abs(tile.position_y - self.y):
                    x_pos = self.calculateClippedXPos(tile, x_pos)
                else:
                    y_pos = self.calculateClippedYPos(tile, y_pos)

        return x_pos, y_pos

    def update(self, delta_time):
        self.movementBehaviorUser(delta_time)

    def draw(self, window):
        if self.rot_image_rect is not None:
            window.blit(self.rot_image, self.rot_image_rect.topleft)