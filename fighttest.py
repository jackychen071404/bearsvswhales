import pygame
import time
import random

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 32)

window_width = 1200
window_height = 800
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("BEARS VS WHALES")

map_width = 2000
map_height = 800

viewport_x = 0
viewport_y = 0

dragging = False
drag_start = (0, 0)

background_image = pygame.image.load("back.png").convert()
background_image = pygame.transform.scale(background_image, (map_width, map_height))

class Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.button_width = 200
        self.button_height = 50
        self.button_x = (window_width - self.button_width) // 2 - 300
        self.button_y = (window_height - self.button_height) // 2 + 300
        self.image = pygame.image.load("button.png")
        self.rect = self.image.get_rect(topleft = (self.button_x,self.button_y))
    #click to add whale
    def update(self,mouse_x,mouse_y,whales):
        if self.rect.collidepoint(mouse_x, mouse_y):
            whales.add(Whale(1900))

class Whale(pygame.sprite.Sprite):
    def __init__(self,x):
        super().__init__()
        self.width = 100
        self.height = 100
        self.x = x
        self.speed = 5
        self.health = 20
        self.attack = 5
        self.atkspeed = 500   #attack every 500 milliseconds
        self.last_attack = pygame.time.get_ticks()   #keep track of time
        self.atkphase = False
        self.image = pygame.image.load('whales.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft = (self.x, 535))
    def move(self):
        self.x -= self.speed
    def hurt(self, towerbear):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack >= self.atkspeed:
            if towerbear.sprite.health > 0:
                towerbear.sprite.health -= 5
                self.last_attack = current_time
    def update(self,viewport_x,towerbear):
        self.viewport_x = viewport_x
        self.move()
        self.rect = self.image.get_rect(topleft=(self.x-self.viewport_x, 535))
        if self.speed == 0: self.atkphase = True
        else: False
        if self.atkphase:
            self.hurt(towerbear)

class Bear(pygame.sprite.Sprite):
    def __init__(self,x):
        super().__init__()
        self.width = 100
        self.height = 100
        self.x = x
        self.speed = 5
        self.health = 20
        self.attack = 5
        self.atkspeed = 500  # attack every 500 milliseconds
        self.last_attack = pygame.time.get_ticks()  # keep track of time
        self.atkphase = False
        self.image = pygame.image.load('bear.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, 535))
    def move(self):
        self.x += self.speed
    def update(self,viewport_x,towerbear):
        self.viewport_x = viewport_x
        self.move()
        self.rect = self.image.get_rect(topleft=(self.x-self.viewport_x, 535))

class Tower(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 200
        self.height = 400
        self.health = 200
        self.maxhealth = 200
        self.image = pygame.image.load("eiffel.jpg")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft = (self.x,self.y))
    def update(self,viewport_x,window):
        self.rect = self.image.get_rect(topleft=(self.x-viewport_x, self.y))
        text = font.render(str(self.health) + " / " + str(self.maxhealth), True, (255,255,255))
        text_rect = self.image.get_rect(topleft = (self.x + self.width/6 - viewport_x,self.y - 50))
        window.blit(text,text_rect)

def collision(units,tower):
    if pygame.sprite.spritecollide(tower.sprite,units,False):
        return True
    else: return False

def stop(units,tower):
    list = pygame.sprite.spritecollide(tower.sprite, units, False)
    for units in list:
        units.speed = 0

clock = pygame.time.Clock()

button = Button()
buttons = pygame.sprite.Group()
buttons.add(button)

whales = pygame.sprite.Group()
bears = pygame.sprite.Group()
bears.add(Bear(50))

tower1 = pygame.sprite.GroupSingle()
tower1.add(Tower(100,250))
tower2 = pygame.sprite.GroupSingle()
tower2.add(Tower(1700,250))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                dragging = True
                drag_start = event.pos
            button.update(mouse_x,mouse_y,whales)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_pos = event.pos
                delta_x = mouse_pos[0] - drag_start[0]
                delta_y = mouse_pos[1] - drag_start[1]  # view different mouse positions
                viewport_x -= delta_x
                viewport_y -= delta_y
                drag_start = mouse_pos

    viewport_x = max(0, min(viewport_x, map_width - window_width))
    viewport_y = max(0, min(viewport_y, map_height - window_height))

        # Render the background image
    window.blit(background_image, (-viewport_x, -viewport_y))
    buttons.draw(window)

    for whale in whales:
        if collision(whales,tower1):
            stop(whales,tower1)

    for bear in bears:
        if collision(bears,tower2):
            stop(bears,tower2)

    tower1.update(viewport_x,window)
    tower1.draw(window)
    tower2.update(viewport_x,window)
    tower2.draw(window)

    whales.update(viewport_x, tower1)
    whales.draw(window)

    bears.update(viewport_x,tower2)
    bears.draw(window)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
