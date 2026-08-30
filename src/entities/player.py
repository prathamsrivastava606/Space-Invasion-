import pygame

from settings import *
from src.entities.bullet import Bullet


class Player:

    def __init__(self):

        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 100

        self.speed = PLAYER_SPEED

        self.image = pygame.image.load(
            "assets/images/playerShip1_blue.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (
                self.width,
                self.height
            )
        )

        self.bullets = []

    def update(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        if self.x < 0:
            self.x = 0

        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width

        for bullet in self.bullets:
            bullet.update()

        self.bullets = [
            bullet for bullet in self.bullets
            if not bullet.off_screen()
        ]

    def shoot(self):

        bullet = Bullet(
            self.x + self.width // 2 - BULLET_WIDTH // 2,
            self.y
        )

        self.bullets.append(bullet)

    def draw(self, screen):

        screen.blit(
            self.image,
            (
                self.x,
                self.y
            )
        )

        for bullet in self.bullets:
            bullet.draw(screen)