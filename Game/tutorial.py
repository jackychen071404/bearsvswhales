import pygame
from object.OK import OK

class Tutorial():
    def __init__(self,window_width,window_height,window,Level):
        self.window_width = window_width
        self.window_height = window_height
        self.window = window
        self.tutorial = pygame.transform.scale(pygame.image.load("../Tower_BGs/tutorial.png"),(window_width,window_height))
        self.Okay = pygame.sprite.GroupSingle()
        self.Okay.add(OK(650,500,0,Level))

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        self.window.blit(self.tutorial,(0,0))
        self.Okay.draw(self.window)
        self.Okay.update(pygame.mouse.get_pos())
