import pygame

class CoinButton(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.button_width = 150 #125
        self.button_height = 63
        self.button_x = x
        self.button_y = y
        self.cost = 100
        self.interval = 100
        self.times = 0
        self.image = pygame.transform.scale(pygame.image.load("../ButtonPics/CoinButton.png"),(180,63))
        self.rect = self.image.get_rect(topleft=(self.button_x, self.button_y))

    def update(self, mouse_x, mouse_y, total_coins):
        total_coins -= self.cost
        return total_coins
