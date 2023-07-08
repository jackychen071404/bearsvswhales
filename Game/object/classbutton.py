import pygame
from object.classwhale import Whale

hand_cursor = pygame.image.load("../Vic,Def/mousehand.png")

class Button(pygame.sprite.Sprite):
    def __init__(self,window,clock,x,y):
        super().__init__()
        self.gamestart = True
        self.window = window
        self.clock = clock
        self.cooldown = 0
        self.mincd = 1000
        self.cost = 50
        self.button_width = 148
        self.button_height = 65
        self.cd_height = 0
        self.button_x = x
        self.button_y = y
        self.image = pygame.image.load("../ButtonPics/button.png")
        self.rect = self.image.get_rect(topleft = (self.button_x,self.button_y))
        #click to add whale
    def timer(self,clock):
        self.cooldown += self.clock.get_time()
        self.clock = clock
        cd_surface = pygame.Surface((self.button_width, self.cd_height), pygame.SRCALPHA)
        cd_surface.fill((0,0,0,128))
        cdrect = cd_surface.get_rect()
        cdrect.topleft = (self.button_x, self.button_y)
        self.window.blit(cd_surface, cdrect)
        if self.cd_height > 0:
            if self.cd_height - (1000/self.mincd) >= 0:
                self.cd_height -= (1000/self.mincd)
    def update(self,mouse_x,mouse_y,whales,total_coins):
        if self.rect.collidepoint(mouse_x, mouse_y):
            if total_coins >= self.cost:
                if self.gamestart:
                    whales.add(Whale(self.window,1700, self.clock))
                    self.cd_height = self.button_height
                    total_coins -= self.cost
                    self.gamestart = False
                    self.cooldown = 0
                else:
                    if self.cooldown >= self.mincd:
                        self.cooldown = 0
                        whales.add(Whale(self.window,1700, self.clock))
                        self.cd_height = self.button_height
                        total_coins -= self.cost
        return total_coins
