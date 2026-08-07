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
enemy = Enemy()

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                player.shoot()

    player.update()

    screen.fill(BLACK)

    enemy.draw(screen)
    player.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()