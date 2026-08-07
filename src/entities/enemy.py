import pygame

from settings import *


class Enemy:

    def __init__(self, x, y):

        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT

        self.x = x
        self.y = y

        self.color = GREEN

    def update(self, direction):

        self.x += direction

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