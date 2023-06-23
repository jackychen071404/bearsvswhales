import pygame
pygame.init()

font = pygame.font.Font('freesansbold.ttf', 32)

window_width = 1200
window_height = 800
window = pygame.display.set_mode((window_width, window_height))

class Bear(pygame.sprite.Sprite):
    cost = 1900
    def __init__(self,x):
        super().__init__()
        self.cost = 50
        self.width = 100
        self.height = 100
        self.x = x
        self.speed = 5
        self.health = 20
        self.maxhealth = 20
        self.attack = 5
        self.atkspeed = 0
        self.atktower = False
        self.atkunit = False
        self.image = pygame.image.load('bear.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, 535))
    def move(self):
        self.x += self.speed
    def hurt(self, tower, whales):
        if self.atkspeed > 60:
            if self.atkunit == True:
                if whales.sprites():
                    whales.sprites()[0].health -= 5
            elif tower.sprite.health > 0:
                tower.sprite.health -= 5
            self.atkspeed = 0
        self.atkspeed += 1
    def update(self,viewport_x,tower, whales):
        self.viewport_x = viewport_x
        self.move()
        self.rect = self.image.get_rect(topleft=(self.x-self.viewport_x, 535))
        if self.atktower or self.atkunit:
            self.hurt(tower, whales)
        text = font.render(str(self.health) + " / " + str(self.maxhealth), True, (255, 255, 255))
        text_rect = self.image.get_rect(topleft=(self.x + self.width / 10 - viewport_x, 300))
        window.blit(text, text_rect)
        if self.health == 0:
            self.kill()
