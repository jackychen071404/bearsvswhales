#4500 x 2592
import pygame
from object.classmapbutton import MapButton

class WorldMap():
    def __init__(self,viewport,window_width,window_height,window):
        self.run = True
        self.map_width = 4500
        self.map_height = 2592
        self.window_width = 1200
        self.window_height = 800
        self.window = pygame.display.set_mode((window_width, window_height))
        self.background_image = pygame.transform.scale(pygame.image.load("../Tower_BGs/worldmap.png").convert(),(self.map_width, self.map_height))
        self.viewport = viewport
        self.mapbuttons = pygame.sprite.Group()
        self.mapbuttons.add(MapButton(400,400))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.viewport.dragging = True
                    self.viewport.drag_start = event.pos
                for button in self.mapbuttons.sprites():
                    if button.rect.collidepoint(mouse_x, mouse_y):
                        self.run = False
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
        self.mapbuttons.update(self.viewport.x,self.viewport.y)

