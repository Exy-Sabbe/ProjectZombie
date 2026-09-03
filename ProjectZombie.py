import pygame
import os
from sys import exit # Terminating the program
from player import *
from map import *
from camera import *
from bullet import *
from zombiemanager import *

# ----CONSTANTS----
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 30
PLAYER_SPEED = 500 # Pixels per second
PLAYER_HEALTH = 100

ZOMBIE_WIDTH = 45
ZOMBIE_HEIGHT = 40
ZOMBIE_SPEED = 400 # Pixels per second
ZOMBIE_HEALTH = 20

BULLET_SPEED = 2500 # Pixels per second
BULLET_LIFETIME = 3 # How long until automatically removed
BULLET_COOLDOWN = 0.2 # How long until you can shoot again
BULLET_DAMAGE = 20

MAP_WIDTH = 40
MAP_HEIGHT = 30
TILE_SIZE = 40

# ----INIT GAME----
# Always initialize pygame!
pygame.init()
# Create window of desired size
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Set name of window
pygame.display.set_caption("Project Zombie")
# Set icon if wished, commented because of code order swapping around
#pygame.display.set_icon(player_image)
# Get clock for FPS handling
clock = pygame.time.Clock()

# ----INIT MAP-----
my_map = Map(MAP_WIDTH, MAP_HEIGHT, TILE_SIZE)

# ---INIT PLAYER---
player = Player(PLAYER_WIDTH, PLAYER_HEIGHT, my_map.GetPixelWidth() / 2, my_map.GetPixelHeight() / 2, PLAYER_SPEED, PLAYER_HEALTH, my_map, os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.join("images", "character.png")), 90)

# ---INIT BULLET MANAGER---
bullet_manager = Bulletmanager(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.join("images", "bullet.png")), 90, BULLET_SPEED, BULLET_LIFETIME, BULLET_COOLDOWN, BULLET_DAMAGE, my_map)

# ---INIT ZOMBIE MANAGER---
zombie_manager = ZombieManager([(100, 500), (200, 400)], ZOMBIE_WIDTH, ZOMBIE_HEIGHT, ZOMBIE_SPEED, ZOMBIE_HEALTH, my_map, os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.join("images", "zombie.png")), 180, 10, 5, 60)

# ---INIT CAMERA---
Camera().SetWindow(window)

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
    # Convert delta_time to seconds instead of milliseconds
    delta_time = clock.get_time() / 1000
    # Update player
    player.Update(delta_time)
    # Update bullets
    bullet_manager.Update(delta_time)
    # Update zombies
    zombie_manager.Update(delta_time)
    # Move camera on top of player again
    Camera().SetCameraPos(player.GetCenterPos())

    # ----DRAW----
    # Draw background
    window.fill("blue")
    # Draw map image
    my_map.Draw()
    # Draw player
    player.Draw()
    # Draw bullets
    bullet_manager.Draw()
    # Draw zombies
    zombie_manager.Draw()

    # Update display every frame
    pygame.display.update()

    # Force game at 60 FPS (basically freeze game loop until enough time has passed for 1 frame)
    clock.tick(60)