import pygame

hand_cursor = pygame.image.load("../Vic,Def/mousehand.png")

class OK(pygame.sprite.Sprite):
    def __init__(self,x,y,value,level,window):
        super().__init__()
        self.window = window
        self.x = x
        self.y = y
        self.image = pygame.image.load("../Vic,Def/OK.png")
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.value = value
        self.level = level
    def update(self,mouse_pos):
        mouse_x,mouse_y = mouse_pos
        if self.rect.collidepoint(mouse_x, mouse_y):
            pygame.mouse.set_visible(False)
            self.window.blit(hand_cursor, pygame.mouse.get_pos())
            if pygame.mouse.get_pressed()[0]:
                if self.value == 0:
                    self.level.tutorialstart = False
                elif self.value == 1:
                    self.level.run = True
        else:
            pygame.mouse.set_visible(True)