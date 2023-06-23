import pygame
import time
import random
from classwhale import Whale
from classbear import Bear
from classbutton import Button
from classtower import Tower

pygame.init()
clock = pygame.time.Clock()
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

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.value = 1
        self.rect = pygame.Rect(x, y, 20, 20)

COIN_GENERATE_EVENT = pygame.USEREVENT + 1
COIN_GENERATE_INTERVAL = 100
coins = pygame.sprite.Group()
total_coins = 0

def generate_coins():
    global total_coins
    for _ in range(1):
        x = random.randint(0, window_width)
        y = random.randint(0, window_height)
        coin = Coin(x, y)
        coins.add(coin)
        total_coins += coin.value

pygame.time.set_timer(COIN_GENERATE_EVENT, COIN_GENERATE_INTERVAL)

def collision(units,tower):
    if pygame.sprite.spritecollide(tower.sprite,units,False):
        return True
    else: return False

def stop(units,tower):
    list = pygame.sprite.spritecollide(tower.sprite, units, False)
    for units in list:
        units.speed = 0
        units.atktower = True

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
        elif event.type == COIN_GENERATE_EVENT:
            generate_coins()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                dragging = True
                drag_start = event.pos
            total_coins = button.update(mouse_x,mouse_y,whales,total_coins)
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

    collides = pygame.sprite.groupcollide(whales, bears, False, False)
    if collides:
        for whale in collides.keys():
            whale.speed = 0
            bear.speed = 0
            whale.atkunit = True
            bear.atkunit = True
    else:
        for bear in bears:
            bear.speed = 5
            bear.atkunit = False
        for whale in whales:
            whale.speed = 5
            whale.atkunit = False

    for whale in whales:
        if collision(whales,tower1):
            stop(whales,tower1)

    for bear in bears:
        if collision(bears,tower2):
            stop(bears,tower2)

    cointext = font.render("Coins: " + str(total_coins), True, (255, 255, 255))
    window.blit(cointext, (10, 10))

    tower1.update(viewport_x,window)
    tower1.draw(window)
    tower2.update(viewport_x,window)
    tower2.draw(window)

    whales.update(viewport_x, tower1,bears)
    whales.draw(window)

    bears.update(viewport_x,tower2,whales)
    bears.draw(window)

    if tower1.sprite.health == 0:
        text = font.render("VICTORY!",True,(0,0,0))
        text_rect = tower1.sprite.image.get_rect(topleft=(600,400))
        window.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
