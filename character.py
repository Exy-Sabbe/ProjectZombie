import pygame
import camera
import math
import map

class Character():
    def __init__(self, width, height, speed, map, image_path, corr_angle = 0):
        self._x = 0
        self._y = 0

        self.__game_width = map.GetPixelWidth()
        self.__game_height = map.GetPixelHeight()
        self.__map = map
        self.__width = width
        self.__height = height
        self.__speed = speed
        self.__half_size = max(self.__width, self.__height) / 2
        image = pygame.image.load(image_path)
        self.__base_image = pygame.transform.scale(image, (self.__width, self.__height))
        self.__image_correction_angle = corr_angle
        self.__rot_image = pygame.transform.rotate(self.__base_image, 0)
        self.__rot_image_rect = None

        self.__should_move_up = False
        self.__should_move_down = False
        self.__should_move_left = False
        self.__should_move_right = False
        self.__should_look_at = (0, 0)

    def GetCenterPos(self):
        return (self._x + self.__width / 2, self._y + self.__height / 2)

    def MoveUp(self):
        self.__should_move_up = True

    def MoveDown(self):
        self.__should_move_down = True

    def MoveLeft(self):
        self.__should_move_left = True

    def MoveRight(self):
        self.__should_move_right = True

    def LookAt(self, position):
        self.__should_look_at = position

    def __CalculateClippedXPos(self, tile, x_pos):
        tile_x = tile.GetXPos()
        tile_size = tile.GetSize()
        if tile_x + tile_size / 2 > x_pos - self.__half_size and tile_x < x_pos:
            return tile_x + tile_size / 2 + self.__half_size
        elif tile_x - tile_size / 2 < x_pos + self.__half_size and tile_x > x_pos:
            return tile_x - tile_size / 2 - self.__half_size
        # Can't normally happen because we already confirmed tile is overlapping in calculateClippedPos
        return x_pos

    def __CalculateClippedYPos(self, tile, y_pos):
        tile_y = tile.GetYPos()
        tile_size = tile.GetSize()
        if tile_y + tile_size / 2 > y_pos - self.__half_size and tile_y < y_pos:
            return tile_y + tile_size / 2 + self.__half_size
        elif tile_y - tile_size / 2 < y_pos + self.__half_size and tile_y > y_pos:
            return tile_y - tile_size / 2 - self.__half_size
        # Can't normally happen because we already confirmed tile is overlapping in calculateClippedPos
        return y_pos

    def __CalculateClippedPos(self, x_pos, y_pos):
        # Create temporary rect with given position to check if it overlaps with any tiles tile
        rect = pygame.Rect(x_pos - self.__half_size, y_pos - self.__half_size, max(self.__width, self.__height), max(self.__width, self.__height))

        # Check all tiles
        for tile in self.__map.GetTiles():
            if tile.IsPassable():
                continue
            
            # If temp rect overlaps with tile, correct either X or Y pos (depending on which overlap is bigger)
            if rect.colliderect(tile.GetRect()):
                if abs(tile.GetXPos() - x_pos) > abs(tile.GetYPos() - y_pos):
                    x_pos = self.__CalculateClippedXPos(tile, x_pos)
                else:
                    y_pos = self.__CalculateClippedYPos(tile, y_pos)

        return x_pos, y_pos
    
    def __Move(self, delta_time):
        # --MOVEMENT--
        # Make speed independant on framerate
        speed = self.__speed * delta_time

        # Determine new temporary position of player (if correct keys are pressed)
        new_x = None
        new_y = None

        if self.__should_move_up and not self.__should_move_down:
            new_y = max(self._y - speed, self.__half_size)
        if self.__should_move_down and not self.__should_move_up:
            new_y = min(self._y + speed, self.__game_height - self.__half_size)
        if self.__should_move_left and not self.__should_move_right:
            new_x = max(self._x - speed, self.__half_size)
        if self.__should_move_right and not self.__should_move_left:
            new_x = min(self._x + speed, self.__game_width - self.__half_size)

        self.__should_move_up = self.__should_move_down = self.__should_move_left = self.__should_move_right = False

        # If player moved, check if the new position overlaps with an impassable tile and correct
        if new_x is not None or new_y is not None:    
            self._x, self._y = self.__CalculateClippedPos(self._x if new_x is None else new_x, self._y if new_y is None else new_y)

        # --ROTATION--
        # Get angle to rotate image (towards mouse)
        player_rect = self.__base_image.get_rect(center = (self._x, self._y))
        mx, my = self.__should_look_at
        dx, dy = mx - player_rect.centerx, my - player_rect.centery
        angle = math.degrees(math.atan2(-dy, dx)) - self.__image_correction_angle

        # Rotate image around center given determined angle
        self.__rot_image = pygame.transform.rotate(self.__base_image, angle)
        self.__rot_image_rect = self.__rot_image.get_rect(center = player_rect.center)

    def Update(self, delta_time):
        self.__Move(delta_time)

    def Draw(self):
        if self.__rot_image_rect is not None:
            camera.Camera().DrawImageOnWorld(self.__rot_image, self.__rot_image_rect)