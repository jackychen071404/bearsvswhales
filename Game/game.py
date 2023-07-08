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
from tutorial import Tutorial
from Level_1 import Level_01_State,Viewport,Wallet

pygame.init()
pygame.display.set_caption("BEARS VS WHALES")
mapmusic = "music/mapmusic.mp3"
gunna = "music/GUNNA.mp3"
map_channel = pygame.mixer.Channel(0)
gunna_channel = pygame.mixer.Channel(1)
map_channel.play(pygame.mixer.Sound(mapmusic),loops=-1,fade_ms=0)
map_channel.set_volume(0)
global track
track = 0

clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
window_width = 1200
window_height = 800
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("BEARS VS WHALES")


running = True
worldmap = WorldMap(window,window_width,window_height,clock,Viewport())
Level1 = Level_01_State(window,window_width,window_height,clock,Viewport(),Wallet(),worldmap)
tutorial = Tutorial(window,window_width,window_height,Level1)
while running:
    if worldmap.run:
        if track == 1:
            gunna_channel.pause()
            map_channel.play(pygame.mixer.Sound(mapmusic),loops=-1,fade_ms=0)
            map_channel.set_volume(0)
            track = 0
        worldmap.handle_events()
        worldmap.update()
    elif Level1.tutorialstart:
        if track == 0:
            map_channel.pause()
            gunna_channel.play(pygame.mixer.Sound(gunna), loops=-1, fade_ms=0)
            gunna_channel.set_volume(0)
            track = 1
        tutorial.draw()
    else:
        if track == 0:
            Level1.restart()
            map_channel.pause()
            gunna_channel.play(pygame.mixer.Sound(gunna), loops=-1, fade_ms=0)
            gunna_channel.set_volume(0)
            track = 1
        Level1.handle_events()
        Level1.update()
    pygame.display.update()
    clock.tick(60)
pygame.quit()