import pygame
from classwhale import Whale
pygame.init()

window_width = 1200
window_height = 800
window = pygame.display.set_mode((window_width, window_height))

class Button(pygame.sprite.Sprite):
    def __init__(self,clock,x,y):
        super().__init__()
        self.gamestart = True
        self.clock = clock
        self.cooldown = 0
        self.mincd = 1200
        self.cost = 50
        self.button_width = 148
        self.button_height = 65
        self.cd_height = 0
        self.button_x = x
        self.button_y = y
        self.image = pygame.image.load("ButtonPics/button.png")
        self.rect = self.image.get_rect(topleft = (self.button_x,self.button_y))
        #click to add whale
    def timer(self,clock,window):
        self.cooldown += self.clock.get_time()
        self.clock = clock
        cd_surface = pygame.Surface((self.button_width, self.cd_height), pygame.SRCALPHA)
        cd_surface.fill((0,0,0,128))
        cdrect = cd_surface.get_rect()
        cdrect.topleft = (self.button_x, self.button_y)
        window.blit(cd_surface, cdrect)
        if self.cd_height > 0:
            if self.cooldown >= (self.mincd / self.button_height)+7:
                self.cd_height -= 1
    def update(self,mouse_x,mouse_y,whales,total_coins):
        if self.rect.collidepoint(mouse_x, mouse_y):
            if total_coins >= self.cost:
                if self.gamestart:
                    whales.add(Whale(1700, self.clock))
                    self.cd_height = self.button_height
                    total_coins -= self.cost
                    self.gamestart = False
                    self.cooldown = 0
                else:
                    if self.cooldown >= self.mincd:
                        self.cooldown = 0
                        whales.add(Whale(1700, self.clock))
                        self.cd_height = self.button_height
                        total_coins -= self.cost
        return total_coins