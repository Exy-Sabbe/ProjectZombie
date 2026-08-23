import pygame
import os
from sys import exit # Terminating the program
from player import *
from map import *

# ----CONSTANTS----
GAME_WIDTH = 800
GAME_HEIGHT = 600

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
game_map = Map(20, 15)

# ---INIT PLAYER---
my_player = Player(game_map, os.path.join(os.path.dirname(os.path.realpath(__file__)), os.path.join("images", "character.png")), 90)

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
    my_player.update(clock.get_time())

    # ----DRAW----
    game_map.draw(window)
    my_player.draw(window)

    # Update display every frame
    pygame.display.update()

    # Force game at 60 FPS (basically freeze game loop until enough time has passed for 1 frame)
    clock.tick()