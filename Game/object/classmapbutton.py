import pygame
pygame.init()

class MapButton(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.button_width = 40
        self.button_height = 40
        self.x = x
        self.y = y
        self.image = pygame.image.load("../ButtonPics/map_button.jpg")
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    def update(self,viewport_x,viewport_y):
        self.rect = self.image.get_rect(topleft=(self.x-viewport_x, self.y-viewport_y))