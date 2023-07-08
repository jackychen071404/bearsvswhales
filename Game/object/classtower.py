import pygame

font = pygame.font.Font(None, 32)

window_width = 1200
window_height = 800
window = pygame.display.set_mode((window_width, window_height))

class Tower(pygame.sprite.Sprite):
    def __init__(self,x,y,string):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 200
        self.height = 400
        self.health = 200
        self.maxhealth = 200
        self.image = pygame.image.load(string)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft = (self.x,self.y))
    def update(self,viewport_x,window,pos):
        self.rect = self.image.get_rect(topleft=(self.x-viewport_x, self.y))
        text = font.render(str(self.health) + " / " + str(self.maxhealth), True, (0,0,0))
        text_rect = self.image.get_rect(topleft = (self.x + self.width/pos - viewport_x,self.y-10))
        window.blit(text,text_rect)