import pygame

class Victory(pygame.sprite.Sprite):
    def __init__(self,string):
        super().__init__()
        self.button_width = 300
        self.button_height = 200
        self.button_x = 600
        self.button_y = 400
        self.image = pygame.image.load(string)
        self.rect = self.image.get_rect(center=(self.button_x, self.button_y))
