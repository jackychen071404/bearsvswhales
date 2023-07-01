import pygame
import time
import random
from classwhale import Whale
from classbear import Bear
from classbutton import Button
from classEmptyButton import EmptyButton
from classbuttons import ButtonSlider
from coinbutton import CoinButton
from classtower import Tower
from coin import Coin

#setting up
pygame.init()
#bg_music = pygame.mixer.Sound("GUNNA.mp3")
#bg_music.play(loops=-1)
#bg_music.set_volume(0.1)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
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
background_image = pygame.image.load("Tower_BGs/back.png").convert()
background_image = pygame.transform.scale(background_image, (map_width, map_height))

#money making
def generate_coins():
    global total_coins
    global max_coins
    for _ in range(1):
        x = random.randint(0, window_width)
        y = random.randint(0, window_height)
        coin = Coin(x, y)
        coins.add(coin)
        if total_coins < max_coins:
            total_coins += coin.value
COIN_GENERATE_EVENT = pygame.USEREVENT + 1
COIN_GENERATE_INTERVAL = 100
coins = pygame.sprite.Group()
total_coins = 0
max_coins = 200
pygame.time.set_timer(COIN_GENERATE_EVENT, COIN_GENERATE_INTERVAL)
coin_icon = pygame.image.load("ButtonPics/moneyIcon.png") #125 x 30
coin_rect = pygame.image.load("ButtonPics/moneyIcon.png").get_rect(topleft=(5, 750)) #125 x 30

def stop(units,tower):
    for units in pygame.sprite.spritecollide(tower.sprite, units, False):
        if units.health > 0:
            units.speed = 0
            units.atktower = True

#adding buttons
buttons = pygame.sprite.Group()
buttons.add(Button(clock,210,710))
buttons.add(EmptyButton(368,710))
buttons.add(EmptyButton(526,710))
buttons.add(EmptyButton(684,710))
buttons.add(EmptyButton(842,710))
buttons.add(CoinButton(5,687))
slider = ButtonSlider()
BS = pygame.sprite.GroupSingle()
BS.add(slider)
#adding units
whales = pygame.sprite.Group()
#enemy spawners
BEAR_GENERATE_EVENT = pygame.USEREVENT + 2
BEAR_GENERATE_INTERVAL = 10000
pygame.time.set_timer(BEAR_GENERATE_EVENT, BEAR_GENERATE_INTERVAL)
bears = pygame.sprite.Group()
bears.add(Bear(50,clock))
#adding towers
tower1 = pygame.sprite.GroupSingle()
tower1.add(Tower(100,250,"Tower_BGs/cntower.png"))
tower2 = pygame.sprite.GroupSingle()
tower2.add(Tower(1700,250,"Tower_BGs/whaletower.png"))

running = True
while running:
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == COIN_GENERATE_EVENT:
            generate_coins()
        elif event.type == BEAR_GENERATE_EVENT:
            bears.add(Bear(50,clock))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                dragging = True
                drag_start = event.pos
            for button in buttons.sprites():
                if type(button) == Button:
                    total_coins = button.update(mouse_x,mouse_y,whales,total_coins) #see if money has been spent
                elif type(button) == CoinButton:
                    if button.rect.collidepoint(mouse_x, mouse_y):
                        if total_coins >= button.cost:
                            button.times += 1
                            if button.times < 9:
                                button.interval -= 10
                                total_coins = button.update(mouse_x, mouse_y, total_coins)
                                max_coins += 50
                            pygame.time.set_timer(COIN_GENERATE_EVENT, button.interval)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_pos = event.pos
                delta_x = mouse_pos[0] - drag_start[0]
                delta_y = mouse_pos[1] - drag_start[1]  # view different mouse positions
                viewport_x -= delta_x
                viewport_y -= delta_y
                drag_start = mouse_pos
    # Render the background image
    viewport_x = max(0, min(viewport_x, map_width - window_width))
    viewport_y = max(0, min(viewport_y, map_height - window_height))
    window.blit(background_image, (-viewport_x, -viewport_y))
    #draw buttons
    BS.draw(window)
    buttons.draw(window)
    for button in buttons.sprites():
        if type(button) == Button:
            button.timer(clock,window)
    #draw monies
    window.blit(coin_icon,coin_rect)
    cointext = font.render("Monies: " + str(total_coins) + "/" + str(max_coins), True, (0, 0, 0))
    window.blit(cointext, (10, 755))
    #check collisions
    for bear in bears:
        if bear.health > 0:
            bear.speed = bear.maxspeed
        bear.atkunit = False
        stop(bears, tower2)
        if len(whales) > 0:
            for whale in whales:
                if pygame.Rect.colliderect(bear.range,whale.rect):
                    if whale.health > 0:
                        bear.speed = 0
                        bear.atkunit = True
                    if bear.health <= 0:
                        bear.speed = -8
    for whale in whales:
        if whale.health > 0:
            whale.speed = whale.maxspeed
        whale.atkunit = False
        stop(whales, tower1)
        if len(bears) > 0:
            for bear in bears:
                if pygame.Rect.colliderect(whale.rect, bear.rect):
                    if bear.health > 0:
                        whale.speed = 0
                        whale.atkunit = True
                    if whale.health <= 0:
                        whale.speed = -8

    #draw guys
    tower1.update(viewport_x,window,2)
    tower1.draw(window)
    tower2.update(viewport_x,window,6)
    tower2.draw(window)
    whales.update(viewport_x, tower1,bears)
    whales.draw(window)
    bears.update(viewport_x,tower2,whales)
    bears.draw(window)
    #victory or defeat
    if tower1.sprite.health == 0:
        text = font.render("VICTORY!",True,(0,0,0))
        text_rect = tower1.sprite.image.get_rect(topleft=(600,400))
        window.blit(text, text_rect)
    if tower2.sprite.health == 0:
        text = font.render("DEFEAT!",True,(0,0,0))
        text_rect = tower1.sprite.image.get_rect(topleft=(600,400))
        window.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()