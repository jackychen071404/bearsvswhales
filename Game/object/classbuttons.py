import pygame

class ButtonSlider(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((800, 100))
        self.surface.fill((150, 75, 0))
        self.image = pygame.image.load("../ButtonPics/buttonholder.png")
        self.rect = self.surface.get_rect(topleft =(200, 700))