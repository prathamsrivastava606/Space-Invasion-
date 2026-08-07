import pygame

from settings import *


class Enemy:

    def __init__(self):

        self.width = 60
        self.height = 60

        self.x = WIDTH // 2 - self.width // 2
        self.y = 80

        self.color = (0, 255, 0)

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