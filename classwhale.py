import pygame
import time
import random
pygame.init()

font = pygame.font.Font('freesansbold.ttf', 32)

window_width = 1200
window_height = 800
window = pygame.display.set_mode((window_width, window_height))

class Whale(pygame.sprite.Sprite):
    def __init__(self,x,clock):
        super().__init__()
        self.width = 100
        self.height = 100
        self.x = x
        self.y = random.randrange(0,4) * 5 + 525
        self.speed = 5
        self.maxspeed = 5
        self.health = 20
        self.maxhealth = 20
        self.attack = 5
        self.atkspeed = 0

        self.clock = clock
        self.atktower = False
        self.atkunit = False
        self.atk_frame0 = pygame.image.load('WhaleAttack/whale_atk0.png').convert_alpha()
        self.atk_frame1 = pygame.image.load('WhaleAttack/whale_atk1.png').convert_alpha()
        self.atk_frame2 = pygame.image.load('WhaleAttack/whale_atk2.png').convert_alpha()
        self.atk_frame3 = pygame.image.load('WhaleAttack/whale_atk3.png').convert_alpha()
        self.atksprites = [self.atk_frame0, self.atk_frame0, self.atk_frame0, self.atk_frame1, self.atk_frame2,
                           self.atk_frame3, self.atk_frame0, self.atk_frame0, self.atk_frame0]
        self.atk_animation_timer = 0
        self.death_animation_timer = 0
        self.deadsprite = pygame.image.load('WhaleAttack/whale_dead.png').convert_alpha()

        self.is_walking = True
        self.whale_frame0 = pygame.image.load('WhaleAnimation/whale_walk0.png').convert_alpha()
        self.whale_frame1 = pygame.image.load('WhaleAnimation/whale_walk1.png').convert_alpha()
        self.sprites = [self.whale_frame0, self.whale_frame1]
        self.current_sprite = 0

        self.image = pygame.transform.scale(self.whale_frame0.convert_alpha(), (self.width, self.height))
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
    def move(self):
        self.x -= self.speed
    def hurt_animate(self):
        frame = 125
        self.atk_animation_timer += self.clock.get_time()
        if self.atk_animation_timer >= frame:
            self.atk_animation_timer = 0
            self.current_sprite = self.current_sprite +  1
            self.image = self.atksprites[self.current_sprite]
        if self.current_sprite >= len(self.atksprites) - 1:
            self.current_sprite = 0
    def hurt(self, tower, bears):
        if self.atkspeed > 60:
            if self.atkunit == True:
                if bears.sprites():
                    bears.sprites()[0].health -= 5
            elif tower.sprite.health > 0:
                tower.sprite.health -= 5
            self.atkspeed = 0
        self.atkspeed += 1
    def death(self,viewport_x):
        if self.health <= 0:
            self.is_walking = False
            frame = 300
            self.death_animation_timer += self.clock.get_time()
            self.image = self.deadsprite
            if self.death_animation_timer >= frame:
                self.death_animation_timer = 0
                self.kill()
    def update(self,viewport_x,tower,bears):
        if self.is_walking:
            self.current_sprite += 0.12
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]
        self.viewport_x = viewport_x
        self.move()
        self.rect = self.image.get_rect(topleft=(self.x-self.viewport_x, self.y))
        if self.atktower or self.atkunit:
            if self.is_walking:
                self.image = self.atksprites[0]
                self.current_sprite = 0
            self.is_walking = False
            self.hurt_animate()
            self.hurt(tower, bears)
        else:
            self.is_walking = True

        text = font.render(str(self.health) + " / " + str(self.maxhealth), True, (255, 255, 255))
        text_rect = self.image.get_rect(topleft=(self.x + self.width / 4 - viewport_x, 300))
        window.blit(text, text_rect)
        self.death(viewport_x)