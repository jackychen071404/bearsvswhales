import pygame
import random

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Coin Class
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.value = 1
        self.rect = pygame.Rect(x, y, 20, 20)

# Create Custom Event for Coin Generation
COIN_GENERATE_EVENT = pygame.USEREVENT + 1

# Set Coin Generation Timer (in milliseconds)
COIN_GENERATE_INTERVAL = 500  # Generate 10 coins every half a second

# Game Loop
running = True
coins = pygame.sprite.Group()
total_coins = 0

# Function to generate coins
def generate_coins():
    global total_coins
    for _ in range(10):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        coin = Coin(x, y)
        coins.add(coin)
        total_coins += coin.value

# Create Coin Generation Timer Event
pygame.time.set_timer(COIN_GENERATE_EVENT, COIN_GENERATE_INTERVAL)

while running:
    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == COIN_GENERATE_EVENT:
            generate_coins()

    # Render
    screen.fill((0, 0, 0))  # Fill the screen with black color

    # Draw Total Coins
    text = font.render("Coins: " + str(total_coins), True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
