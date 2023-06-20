import pygame
import time
import random

pygame.init()

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
    def updater(self,mouse_x,mouse_y):
        if self.rect.collidepoint(mouse_x, mouse_y):
            print("hi")
class Whale(pygame.sprite.Sprite):
    def __init__(self,viewport_x,whale_x):
        super().__init__()
        self.width = 100
        self.height = 100
        self.whale_x = whale_x
        self.speed = 5
        self.viewport_x = viewport_x
        self.image = pygame.image.load('whales.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft = (self.whale_x-self.viewport_x, 535))
    def move(self):
        self.whale_x -= self.speed
    def update(self,viewport_x,tower):
        self.viewport_x = viewport_x
        self.rect = self.image.get_rect(topleft=(self.whale_x - self.viewport_x, 535))
        self.move()
class Tower(pygame.sprite.Sprite):
    def __init__(self,viewport_x,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 200
        self.height = 400
        self.image = pygame.image.load("eiffel.jpg")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft = (self.x-viewport_x,self.y))
    def update(self,viewport_x):
        self.rect = self.image.get_rect(topleft=(self.x - viewport_x, self.y))

def collision(whales,tower1):
    pass
clock = pygame.time.Clock()

button = Button()
buttons = pygame.sprite.Group()
buttons.add(button)

whales = pygame.sprite.Group()
whales.add(Whale(0,1900))

tower1 = pygame.sprite.GroupSingle()
tower1.add(Tower(0,100,250))
tower2 = pygame.sprite.GroupSingle()
tower2.add(Tower(0,1700,250))

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
            button.updater(mouse_x,mouse_y)
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

    tower1.update(viewport_x)
    tower1.draw(window)
    tower2.update(viewport_x)
    tower2.draw(window)
    #if whale_x < -50: whale_x = 1900
    #whale_screen_x = whale_x - viewport_x
    #whale_rect.x = whale_screen_x
    #window.blit(whale_surface, whale_rect)
    whales.update(viewport_x,tower1)
    whales.draw(window)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
