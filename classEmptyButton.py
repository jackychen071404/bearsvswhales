import pygame
pygame.init()

class EmptyButton(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.button_width = 148
        self.button_height = 65
        self.button_x = x
        self.button_y = y
        self.image = pygame.image.load("ButtonPics/emptybutton.png")
        self.rect = self.image.get_rect(topleft=(self.button_x, self.button_y))