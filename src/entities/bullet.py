import pygame

from settings import *


class Bullet:

    def __init__(self, x, y):

        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT

        self.x = x
        self.y = y

        self.speed = BULLET_SPEED

        self.color = RED

    def update(self):

        self.y -= self.speed

    def draw(self, screen):

        pygame.draw.rect(
            screen,
            self.color,
            (self.x, self.y, self.width, self.height)
        )

    def get_rect(self):

        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def off_screen(self):

        return self.y < -self.height