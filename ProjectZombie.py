import pygame
import os
from sys import exit # Terminating the program
from player import *
from map import *
from camera import *
from bullet import *

# ----CONSTANTS----
GAME_WIDTH = 800
GAME_HEIGHT = 600

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 30
PLAYER_SPEED = 500 # Pixels per second

BULLET_SPEED = 1000 # Pixels per second
BULLET_LIFETIME = 3 # How long until automatically removed
BULLET_COOLDOWN = 0.5 # How long until you can shoot again

MAP_WIDTH = 20
MAP_HEIGHT = 15
TILE_SIZE = 40

# ----INIT GAME----
# Always initialize pygame!
pygame.init()
# Create window of desired size
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
# Set name of window
pygame.display.set_caption("Project Zombie")
# Set icon if wished, commented because of code order swapping around
#pygame.display.set_icon(player_image)
# Get clock for FPS handling
clock = pygame.time.Clock()

# ----INIT MAP-----
map = Map(MAP_WIDTH, MAP_HEIGHT, TILE_SIZE)

# ---INIT PLAYER---
player = Player(PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, map, os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.join("images", "character.png")), 90)

# ---INIT BULLET MANAGER---
bullet_manager = Bulletmanager(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.join("images", "bullet.png")), 90, BULLET_SPEED, BULLET_LIFETIME, BULLET_COOLDOWN)

# ---INIT CAMERA---
camera = Camera()
camera.SetWindow(window)

# ----GAME LOOP----
while True:
    # Event handler (like inputs)
    for event in pygame.event.get():
        # If user clicks X button on window
        if event.type == pygame.QUIT:
            # Stop both pygame running & quit program
            pygame.quit()
            exit()

    # ----UPDATE----
    delta_time = clock.get_time() / 1000
    player.Update(delta_time)
    bullet_manager.Update(delta_time)
    camera.SetCameraPos(player.GetCenterPos())

    # ----DRAW----
    window.fill("blue")
    map.Draw()
    player.Draw()
    bullet_manager.Draw()

    # Update display every frame
    pygame.display.update()

    # Force game at 60 FPS (basically freeze game loop until enough time has passed for 1 frame)
    clock.tick(60)