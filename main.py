import pygame
import sys

from settings import *
from src.entities.player import Player
from src.entities.enemy import Enemy

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()

# Font for score
font = pygame.font.SysFont("Arial", 32)

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

score = 0

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
    # Collision
    # -------------------------

    for bullet in player.bullets[:]:

        for enemy in enemies[:]:

            if bullet.get_rect().colliderect(enemy.get_rect()):

                player.bullets.remove(bullet)
                enemies.remove(enemy)

                score += 10

                break

    # -------------------------
    # Draw
    # -------------------------

    screen.fill(BLACK)

    # Draw enemies
    for enemy in enemies:
        enemy.draw(screen)

    # Draw player
    player.draw(screen)

    # Draw score
    score_text = font.render(f"Score : {score}", True, WHITE)
    screen.blit(score_text, (20, 20))

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()