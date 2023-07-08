#4500 x 2592
import pygame
from object.classmapbutton import MapButton

hand_cursor = pygame.image.load("../Vic,Def/mousehand.png")
#startmusic = pygame.mixer.Sound("music/startmusic.mp3")
#startmusic.set_volume(0.3)

class WorldMap():
    def __init__(self,window,window_width,window_height,clock,viewport):
        self.window = window
        self.window_width = 1200
        self.window_height = 800
        self.clock = clock
        self.map_width = 4500
        self.map_height = 2592
        self.viewport = viewport
        self.background_image = pygame.transform.scale(pygame.image.load("../Tower_BGs/worldmap.png").convert(),
                                                       (self.map_width, self.map_height))
        self.run = True #check if the worldmap is running
        #animations for, battle start!, black screen, and sound effect
        self.battle_start = pygame.image.load("../Vic,Def/Battle_start!.jpg").convert()
        self.start_x = 1200
        self.start_timer = 0
        self.play_start = False
        self.black_height = 0
        self.black_rect = pygame.Surface((1200, self.black_height))
        self.black_rect.fill((0,0,0))
        self.black_timer = 0
        self.songplay = True
        #map buttons
        self.mapbuttons = pygame.sprite.Group()
        self.mapbuttons.add(MapButton(400, 400))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif not self.play_start:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        self.viewport.dragging = True
                        self.viewport.drag_start = event.pos
                    for button in self.mapbuttons.sprites():
                        if button.rect.collidepoint(mouse_x, mouse_y):
                            self.play_start = True
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
        self.viewport.x = max(0, min(self.viewport.x, self.map_width - self.window_width))
        self.viewport.y = max(0, min(self.viewport.y, self.map_height - self.window_height))
        self.window.blit(self.background_image, (-self.viewport.x, -self.viewport.y))
        self.mapbuttons.draw(self.window)
        self.mapbuttons.update(self.viewport.x, self.viewport.y)
        if self.play_start and self.start_x != 0:
            """if self.songplay:
                startmusic.play()
                self.songplay = False"""
            self.window.blit(self.battle_start, (self.start_x, 400))
            self.start_x -= 50
        elif self.play_start:
            self.window.blit(self.battle_start, (self.start_x, 400))
            self.start_timer += self.clock.get_time()
            if self.start_timer >= 500:
                self.black_height += 50
                self.black_rect = pygame.Surface((1200, self.black_height))
                self.window.blit(self.black_rect, (0,0))
                self.black_timer += self.clock.get_time()
                if self.black_timer >= 500:
                    self.run = False
                    self.restart()
        self.detect_mouse()

    def restart(self):
        self.play_start = False
        self.start_x = 1200
        self.start_timer = 0
        self.black_timer = 0
        self.black_height = 0
        self.black_rect = pygame.Surface((1200, 0))
        self.songplay = True

    def detect_mouse(self):
        for button in self.mapbuttons.sprites():
            if button.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_visible(False)
                self.window.blit(hand_cursor, pygame.mouse.get_pos())
            else:
                pygame.mouse.set_visible(True)


