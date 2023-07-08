import pygame

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.value = 1
        self.rect = pygame.Rect(x, y, 10, 10)
        self.monies = 0