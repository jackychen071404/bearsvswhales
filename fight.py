import pygame

pygame.init()

bg_music = pygame.mixer.Sound("We Fly High (Ballin').mp3")
bg_music.play(loops=-1)
bg_music.set_volume(0.1)

window_width = 1200
window_height = 800
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("BEARS VS WHALES")

map_width = 2000
map_height = 800

viewport_x = 0
viewport_y = 0

#tower1
tower1_x = 100
tower1_y = 250
tower1_width = 200
tower1_length = 400

tower1_image = pygame.image.load("eiffel.jpg")
tower1_image = pygame.transform.scale(tower1_image, (tower1_width, tower1_length))

#tower2
tower2_x = 1700
tower2_y = 250

tower2_image = pygame.image.load("eiffel.jpg")
tower2_image = pygame.transform.scale(tower1_image, (tower1_width, tower1_length))

#button
button_width = 200
button_height = 50
button_x = (window_width - button_width) // 2 - 300
button_y = (window_height - button_height) // 2 + 300
button_color = (100,100,100)
button_font = pygame.font.Font(None,30)
button_text = "Basic Whale"

#whale
whales = []

whale_start = 1900
whale_y = 500
whale_width = 100
whale_length = 100
whale_speed = 5
whale_added = False
whale_spawned = False

whale_image = pygame.image.load('whales.png').convert_alpha()
whale_image = pygame.transform.scale(whale_image, (whale_width, whale_length))

#dragging mouse
dragging = False
drag_start = (0, 0)

background_image = pygame.image.load("back.png").convert()
background_image = pygame.transform.scale(background_image, (map_width, map_height))

clock = pygame.time.Clock()
#spawn a whale
def add_whale():
    whale_x = 1900
    whales.append([whale_x,whale_speed])
def spawn(whales):
    for whale in whales:
        [whale_x, whale_speed] = whale
        if crash(whale[0]):
            whale[1] = 0
        whale[0] -= whale[1]

        whale_screen_x = whale_x - viewport_x
        whale_screen_y = whale_y - viewport_y
        window.blit(whale_image, (whale_screen_x, whale_screen_y))

#whale crashes into tower
def crash(whale_x):
    if whale_x + whale_width == tower1_width*1.5 + tower1_x:
        return True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse events
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                dragging = True
                drag_start = event.pos
            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                whale_spawned = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_pos = event.pos
                delta_x = mouse_pos[0] - drag_start[0]
                delta_y = mouse_pos[1] - drag_start[1] #view different mouse positions
                viewport_x -= delta_x
                viewport_y -= delta_y
                drag_start = mouse_pos

    viewport_x = max(0, min(viewport_x, map_width - window_width))
    viewport_y = max(0, min(viewport_y, map_height - window_height))

    # Render the background image
    window.blit(background_image, (-viewport_x, -viewport_y))

    # render button
    pygame.draw.rect(window, button_color, (button_x, button_y, button_width, button_height))
    button_text_render = button_font.render(button_text, True, (255, 255, 255))  # White text
    button_text_rect = button_text_render.get_rect(center=(button_x + button_width / 2, button_y + button_height / 2))
    window.blit(button_text_render, button_text_rect)

    #render tower1
    tower1_screen_x = tower1_x - viewport_x
    tower1_screen_y = tower1_y - viewport_y
    window.blit(tower1_image, (tower1_screen_x, tower1_screen_y))

    #render tower2
    tower2_screen_x = tower2_x - viewport_x
    tower2_screen_y = tower2_y - viewport_y
    window.blit(tower2_image, (tower2_screen_x, tower2_screen_y))

    if whale_spawned:
        add_whale()
        whale_added = True
        whale_x = whale_start
    if whale_added:
        spawn(whales)
    whale_spawned = False
    # Update the display
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
