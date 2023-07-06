import pygame
import time
import random
pygame.init()

font = pygame.font.Font('freesansbold.ttf', 32)

window_width = 1200
window_height = 800
window = pygame.display.set_mode((window_width, window_height))

class Bear(pygame.sprite.Sprite):
    def __init__(self,x,clock):
        super().__init__()
        #stats
        self.width = 100
        self.height = 200
        self.x = x
        self.y = random.randrange(0,4) * 5 + 425
        self.speed = 5
        self.maxspeed = 5
        self.health = 20
        self.maxhealth = 20
        self.KB_count = 1
        self.KB_state = False
        self.attack = 5
        self.atkspeed = 0
        #attacking
        self.clock = clock
        self.atktower = False
        self.atkunit = False
        self.atk_frame0 = pygame.image.load('../BearAttack/bearatk_0.png').convert_alpha()
        self.atk_frame1 = pygame.image.load('../BearAttack/bearatk_1.png').convert_alpha()
        self.atk_frame2 = pygame.image.load('../BearAttack/bearatk_2.png').convert_alpha()
        self.atk_frame3 = pygame.image.load('../BearAttack/bearatk_3.png').convert_alpha()
        self.atksprites = [self.atk_frame0,self.atk_frame0,self.atk_frame0,self.atk_frame1,self.atk_frame2,self.atk_frame3,self.atk_frame0,self.atk_frame0,self.atk_frame0]
        self.deadsprite = pygame.image.load('../BearAttack/beardead.png').convert_alpha()
        self.deadrect = self.deadsprite.get_rect(topleft=(self.x, self.y))
        #walking
        self.is_walking = True
        self.bear_frame0 = pygame.image.load('../BearWalk/Frames/Bear_0000.png').convert_alpha()
        self.bear_frame1 = pygame.image.load('../BearWalk/Frames/Bear_0001.png').convert_alpha()
        self.bear_frame2 = pygame.image.load('../BearWalk/Frames/Bear_0002.png').convert_alpha()
        self.bear_frame3 = pygame.image.load('../BearWalk/Frames/Bear_0003.png').convert_alpha()
        self.bear_frame4 = pygame.image.load('../BearWalk/Frames/Bear_0004.png').convert_alpha()
        self.bear_frame5 = pygame.image.load('../BearWalk/Frames/Bear_0005.png').convert_alpha()
        self.sprites = [self.bear_frame0,self.bear_frame1,self.bear_frame2,self.bear_frame3,self.bear_frame4,self.bear_frame1]
        self.current_sprite = 0
        self.atk_animation_timer = 0
        #dead
        self.is_dead = False
        self.death_animation_timer = 0
        self.bounty = 10
        #load it up
        self.image = pygame.transform.scale(self.bear_frame0, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.range = pygame.Rect(self.x, self.y, self.width, self.height)
    def move(self):
        self.x += self.speed
    def hurt_animate(self):
        frame = 125
        self.atk_animation_timer += self.clock.get_time()
        if self.atk_animation_timer >= frame:
            self.atk_animation_timer = 0
            self.current_sprite = self.current_sprite +  1
            self.image = self.atksprites[self.current_sprite]
        if self.current_sprite >= len(self.atksprites) - 1:
            self.current_sprite = 0
    def hurt(self, tower, whales):
        if self.atkspeed > 60: #attacking every second
            if self.atktower == True:
                if tower.sprite.health > 0:
                    tower.sprite.health -= 5
            elif self.atkunit == True:
                if len(whales) > 0:
                    whales[0].health -= 5
            self.atkspeed = 0
        self.atkspeed += 1
    def knockback(self,viewport_x):
        self.KB_state = True
        self.atkunit = False
        self.atktower = False
        frame = 300
        self.death_animation_timer += self.clock.get_time()
        self.image = self.deadsprite
        if self.death_animation_timer >= frame:
            self.death_animation_timer = 0
            self.KB_state = False
            self.KB_count -= 1
            self.atkspeed = 0
            self.current_sprite = 0
    def death(self,viewport_x):
        self.is_walking = False
        frame = 300
        self.death_animation_timer += self.clock.get_time()
        self.image = self.deadsprite
        if self.death_animation_timer >= frame:
            self.death_animation_timer = 0
            self.kill()
    def update(self,viewport_x,tower, whales):
        print(self.atkspeed)
        if self.is_walking:
            self.current_sprite += 0.12
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]

        self.viewport_x = viewport_x
        self.move()
        self.rect = self.image.get_rect(topleft=(self.x-self.viewport_x, self.y))
        self.range = pygame.Rect(self.x - self.viewport_x, self.y, self.width, self.height)

        if self.atktower or self.atkunit:
            if self.is_walking:
                self.image = self.atksprites[0]
                self.current_sprite = 0
            self.is_walking = False
            self.hurt_animate()
            self.hurt(tower, whales)
        elif not self.KB_state:
            self.is_walking = True

        text = font.render(str(self.health) + " / " + str(self.maxhealth), True, (255, 255, 255))
        text_rect = self.image.get_rect(topleft=(self.x + self.width / 10 - viewport_x, 300))
        window.blit(text, text_rect)
        if self.health <= 0:
            self.death(viewport_x)
        """if self.health <= 10 and self.KB_count == 1:
            self.knockback(viewport_x)"""