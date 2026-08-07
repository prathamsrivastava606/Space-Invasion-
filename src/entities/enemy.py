import pygame

from settings import *


class Enemy:

    def __init__(self, x, y):

        self.width = 60
        self.height = 60

        self.x = x
        self.y = y

        self.color = (0, 255, 0)

    def update(self, direction):

        self.x += direction

    def draw(self, screen):

        pygame.draw.rect(
            screen,
            self.color,
            (
                self.x,
                self.y,
                self.width,
                self.height
            )
        )