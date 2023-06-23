import pygame
from classwhale import Whale
pygame.init()

window_width = 1200
window_height = 800
window = pygame.display.set_mode((window_width, window_height))

class Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cost = 50
        self.button_width = 200
        self.button_height = 50
        self.button_x = (window_width - self.button_width) // 2 - 300
        self.button_y = (window_height - self.button_height) // 2 + 300
        self.image = pygame.image.load("button.png")
        self.rect = self.image.get_rect(topleft = (self.button_x,self.button_y))
    #click to add whale
    def update(self,mouse_x,mouse_y,whales,total_coins):
        if self.rect.collidepoint(mouse_x, mouse_y):
            if total_coins > self.cost:
                whales.add(Whale(1900))
                total_coins -= self.cost

        return total_coins
