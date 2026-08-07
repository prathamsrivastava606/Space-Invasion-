import pygame
import sys

from settings import *
from src.entities.player import Player
from src.entities.enemy import Enemy

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()

player = Player()

# -------------------------
# Enemy Formation
# -------------------------

enemies = []

ROWS = 2
COLUMNS = 7

START_X = 180
START_Y = 80

GAP_X = 100
GAP_Y = 90

for row in range(ROWS):
    for col in range(COLUMNS):

        x = START_X + col * GAP_X
        y = START_Y + row * GAP_Y

        enemies.append(Enemy(x, y))

enemy_speed = 2
enemy_drop = 40

running = True

while running:

    # -------------------------
    # Events
    # -------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                player.shoot()

    # -------------------------
    # Update
    # -------------------------

    player.update()

    for enemy in enemies:
        enemy.update(enemy_speed)

    # Check if formation hits an edge
    hit_edge = False

    for enemy in enemies:

        if enemy.x <= 0 or enemy.x + enemy.width >= WIDTH:
            hit_edge = True
            break

    if hit_edge:

        enemy_speed *= -1

        for enemy in enemies:
            enemy.y += enemy_drop

    # -------------------------
    # Draw
    # -------------------------

    screen.fill(BLACK)

    for enemy in enemies:
        enemy.draw(screen)

    player.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()