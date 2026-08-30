import pygame
import camera
import math
import map

class Character():
    def __init__(self, width, height, speed, map, image_path, corr_angle):
        self._x = 0
        self._y = 0

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

        self.__move_dir = (0, 0)
        self.__should_look_at = (0, 0)

    def GetCenterPos(self):
        return (self._x, self._y)

    def GetForwardsDirection(self):
        return (self.__should_look_at[0] - self._x, self.__should_look_at[1] - self._y)

    def SetMoveDirection(self, direction):
        self.__move_dir = direction

    def LookAt(self, position):
        self.__should_look_at = position

    def __CalculateClippedXPos(self, tile, x_pos):
        tile_x = tile.GetXPos()
        tile_size = tile.GetSize()
        # If tile overlaps with player being on the right
        if tile_x + tile_size / 2 > x_pos - self.__half_size and tile_x < x_pos:
            return tile_x + tile_size / 2 + self.__half_size
        # If tile overlaps with player being on the left
        elif tile_x - tile_size / 2 < x_pos + self.__half_size and tile_x > x_pos:
            return tile_x - tile_size / 2 - self.__half_size
        # Can't normally happen because we already confirmed tile is overlapping in calculateClippedPos
        return x_pos

    def __CalculateClippedYPos(self, tile, y_pos):
        tile_y = tile.GetYPos()
        tile_size = tile.GetSize()
        # If tile overlaps with player being above
        if tile_y + tile_size / 2 > y_pos - self.__half_size and tile_y < y_pos:
            return tile_y + tile_size / 2 + self.__half_size
        # If tile overlaps with player being below
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
        if self.__move_dir != (0, 0):
            # Make speed independant on framerate
            speed = self.__speed * delta_time

            # Normalize move direction
            length = math.sqrt(self.__move_dir[0]**2 + self.__move_dir[1]**2)
            self.__move_dir = (self.__move_dir[0] / length, self.__move_dir[1] / length)

            # Determine new temporary position of player (if correct keys are pressed)
            new_x = self._x + self.__move_dir[0] * speed
            new_y = self._y + self.__move_dir[1] * speed

            # Check if the new position overlaps with an impassable tile and correct 
            self._x, self._y = self.__CalculateClippedPos(self._x if new_x is None else new_x, self._y if new_y is None else new_y)

            # Reset move direction
            self.__move_dir = (0, 0)

        # --ROTATION--
        # Get angle to rotate image (towards mouse)
        player_rect = self.__base_image.get_rect(center = self.GetCenterPos())
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