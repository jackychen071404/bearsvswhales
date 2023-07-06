import pygame
import time
import random
from object.classwhale import Whale
from object.classbear import Bear
from object.classbutton import Button
from object.classEmptyButton import EmptyButton
from object.classbuttons import ButtonSlider
from object.coinbutton import CoinButton
from object.classtower import Tower
from object.coin import Coin
from object.Victory import Victory
from object.OK import OK
from worldmap import WorldMap

#setting up
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
window_width = 1200
window_height = 800
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("BEARS VS WHALES")
BS = pygame.sprite.GroupSingle()
BS.add(ButtonSlider())
Vict = pygame.sprite.GroupSingle()
Vict.add(Victory("../Vic,Def/victory.png"))
Def = pygame.sprite.GroupSingle()
Def.add(Victory("../Vic,Def/defeat.png"))

class Viewport():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dragging = False
        self.drag_start = (0,0)

class Wallet():
    def __init__(self):
        self.total_coins = 0
        self.max_coins = 200
    def update(self):
        if self.total_coins > self.max_coins:
            self.total_coins = self.max_coins

class Level_01_State:
    def __init__(self,viewport,wallet,clock,worldmap):
        self.clock = clock
        self.tutorialstart = True
        self.gamestart = True

        self.map_width = 2000
        self.map_height = 800
        self.background_image = pygame.transform.scale(pygame.image.load("../Tower_BGs/winterbackground.png").convert(), (self.map_width, self.map_height))
        self.viewport = viewport
        #money
        self.wallet = wallet
        self.coins = pygame.sprite.Group()
        self.COIN_GENERATE_EVENT = pygame.USEREVENT + 1
        self.COIN_GENERATE_INTERVAL = 100
        self.coin_icon = pygame.transform.scale(pygame.image.load("../ButtonPics/moneyIcon.png"),(180,30))
        self.coin_rect = pygame.image.load("../ButtonPics/moneyIcon.png").get_rect(topleft=(5, 750))
        #towers
        self.tower1 = pygame.sprite.GroupSingle()
        self.tower2 = pygame.sprite.GroupSingle()

        self.buttons = pygame.sprite.Group()

        self.bears = pygame.sprite.Group()
        self.BEAR_GENERATE_EVENT = pygame.USEREVENT + 2
        self.BEAR_GENERATE_INTERVAL = 10000 #30000
        self.whales = pygame.sprite.Group()
        self.whales_collide_bear = []
        self.bears_collide_whale = []
        self.Okay = pygame.sprite.GroupSingle()
        self.Okay.add(OK(600, 550, 1,worldmap))

    def generate_coins(self):
        for _ in range(1):
            x = random.randint(0, window_width)
            y = random.randint(0, window_height)
            coin = Coin(x, y)
            self.coins.add(coin)
            if self.wallet.total_coins < self.wallet.max_coins:
                self.wallet.total_coins += coin.value

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == self.COIN_GENERATE_EVENT:
                self.generate_coins()
            elif event.type == self.BEAR_GENERATE_EVENT:
                self.bears.add(Bear(50, self.clock))
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.viewport.dragging = True
                    self.viewport.drag_start = event.pos
                for button in self.buttons.sprites():
                    if type(button) == Button:
                        self.wallet.total_coins = button.update(mouse_x, mouse_y, self.whales,
                                                           self.wallet.total_coins)  # see if money has been spent
                    elif type(button) == CoinButton:
                        if button.rect.collidepoint(mouse_x, mouse_y):
                            if self.wallet.total_coins >= button.cost:
                                button.times += 1
                                if button.times < 9:
                                    button.interval -= 10
                                    self.wallet.total_coins = button.update(mouse_x, mouse_y, self.wallet.total_coins)
                                    self.wallet.max_coins += 50
                                pygame.time.set_timer(self.COIN_GENERATE_EVENT, button.interval)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse
                    self.viewport.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if self.viewport.dragging:
                    mouse_pos = event.pos
                    delta_x = mouse_pos[0] - self.viewport.drag_start[0]
                    delta_y = mouse_pos[1] - self.viewport.drag_start[1]  # view different mouse positions
                    self.viewport.x -= delta_x
                    self.viewport.y -= delta_y
                    self.viewport.drag_start = mouse_pos
    def update(self):
        if self.gamestart: #add in things in the start
            self.buttons.add(Button(self.clock, 210, 710))
            self.buttons.add(EmptyButton(368, 710))
            self.buttons.add(EmptyButton(526, 710))
            self.buttons.add(EmptyButton(684, 710))
            self.buttons.add(EmptyButton(842, 710))
            self.buttons.add(CoinButton(5, 687))
            self.bears.add(Bear(50, self.clock))
            self.tower1.add(Tower(100, 250, "../Tower_BGs/cntower.png"))
            self.tower2.add(Tower(1700, 250, "../Tower_BGs/whaletower.png"))
            pygame.time.set_timer(self.COIN_GENERATE_EVENT, self.COIN_GENERATE_INTERVAL) #set timers
            pygame.time.set_timer(self.BEAR_GENERATE_EVENT, self.BEAR_GENERATE_INTERVAL)
            self.gamestart = False
        self.viewport.x = max(0, min(self.viewport.x, self.map_width - window_width))
        self.viewport.y = max(0, min(self.viewport.y, self.map_height - window_height))
        window.blit(self.background_image, (-self.viewport.x, -self.viewport.y))

        BS.draw(window) #draw buttons and put timers on them
        self.buttons.draw(window)
        for button in self.buttons.sprites():
            if type(button) == Button:
                button.timer(self.clock, window)

        window.blit(self.coin_icon, self.coin_rect) #draw money
        cointext = font.render("Monies: " + str(self.wallet.total_coins) + "/" + str(self.wallet.max_coins), True, (0, 0, 0))
        window.blit(cointext, (10, 755))
        self.wallet.update()

        for bear in self.bears: # check collisions
            self.whales_collide_bear = pygame.sprite.spritecollide(bear, self.whales, False)
            if bear.health > 0 and not bear.KB_state:
                bear.speed = bear.maxspeed
            bear.atkunit = False
            self.stop(self.bears, self.tower2)
            if len(self.whales) > 0:
                for whale in self.whales:
                    if pygame.Rect.colliderect(bear.range, whale.rect):
                        if whale.health > 0 and not bear.KB_state:
                            bear.speed = 0
                            bear.atkunit = True
                        """if bear.health <= 10 and bear.KB_count == 1:
                            bear.speed = -30"""
                        if bear.health <= 0:
                            bear.speed = -8
                            if not bear.is_dead:
                                self.wallet.total_coins += bear.bounty
                                bear.is_dead = True
        for whale in self.whales:
            self.bears_collide_whale = pygame.sprite.spritecollide(whale, self.bears, False)
            if whale.health > 0:
                whale.speed = whale.maxspeed
            whale.atkunit = False
            self.stop(self.whales, self.tower1)
            if len(self.bears) > 0:
                for bear in self.bears:
                    if pygame.Rect.colliderect(whale.rect, bear.rect):
                        if bear.health > 0 and not bear.KB_state:
                            whale.speed = 0
                            whale.atkunit = True
                        if whale.health <= 0:
                            whale.speed = -8
        # draw guys
        self.tower1.update(self.viewport.x, window, 2)
        self.tower1.draw(window)
        self.tower2.update(self.viewport.x, window, 6)
        self.tower2.draw(window)
        self.whales.update(self.viewport.x, self.tower1, self.bears_collide_whale)
        self.whales.draw(window)
        self.bears.update(self.viewport.x, self.tower2, self.whales_collide_bear)
        self.bears.draw(window)
        # victory or defeat
        if self.tower1.sprite.health == 0:
            for bear in self.bears:
                bear.kill()
            Vict.draw(window)
            self.Okay.draw(window)
            self.Okay.update(pygame.mouse.get_pos())
        if self.tower2.sprite.health == 0:
            for whale in self.whales:
                whale.kill()
            Def.draw(window)
            self.Okay.draw(window)
            self.Okay.update(pygame.mouse.get_pos())

    def stop(self,units,tower):
        for units in pygame.sprite.spritecollide(tower.sprite, units, False):
            if units.health > 0 and not units.KB_state:
                units.speed = 0
                units.atktower = True

    def restart(self):
        for whale in self.whales:
            whale.kill()
        for bear in self.bears:
            bear.kill()
        for tower in self.tower1:
            tower.kill()
        for tower in self.tower2:
            tower.kill()
        for button in self.buttons:
            button.kill()
        self.wallet.total_coins = 0
        self.wallet.max_coins = 200
        self.COIN_GENERATE_INTERVAL = 100

        self.tutorialstart = True
        self.gamestart = True
