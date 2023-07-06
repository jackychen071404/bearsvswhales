import pygame

class OK(pygame.sprite.Sprite):
    def __init__(self,x,y,value,level):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load("../Vic,Def/OK.png")
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.value = value
        self.level = level
    def update(self,mouse_pos):
        mouse_x,mouse_y = mouse_pos
        if self.rect.collidepoint(mouse_x, mouse_y):
            if pygame.mouse.get_pressed()[0]:
                if self.value == 0:
                    self.level.tutorialstart = False
                elif self.value == 1:
                    self.level.run = True