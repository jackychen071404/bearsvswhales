import pygame
import time
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
        self.speed = 5
        self.maxspeed = 5
        self.health = 20
        self.maxhealth = 20
        self.attack = 5
        self.atkspeed = 0
        #attacking
        self.atktower = False
        self.atkunit = False
        self.atk_frame0 = pygame.image.load('BearAttack/bearatk_0.png').convert_alpha()
        self.atk_frame1 = pygame.image.load('BearAttack/bearatk_1.png').convert_alpha()
        self.atk_frame2 = pygame.image.load('BearAttack/bearatk_2.png').convert_alpha()
        self.atk_frame3 = pygame.image.load('BearAttack/bearatk_3.png').convert_alpha()
        self.atksprites = [self.atk_frame0,self.atk_frame1,self.atk_frame2,self.atk_frame3]
        self.current_atk = 0
        self.fight_start_time = 0
        self.deadsprite = pygame.image.load('BearAttack/beardead.png').convert_alpha()
        self.deadrect = self.deadsprite.get_rect(topleft=(self.x, 435))
        #walking
        self.is_walking = True
        self.bear_frame0 = pygame.image.load('Frames/Bear_0000.png').convert_alpha()
        self.bear_frame1 = pygame.image.load('Frames/Bear_0001.png').convert_alpha()
        self.bear_frame2 = pygame.image.load('Frames/Bear_0002.png').convert_alpha()
        self.bear_frame3 = pygame.image.load('Frames/Bear_0003.png').convert_alpha()
        self.bear_frame4 = pygame.image.load('Frames/Bear_0004.png').convert_alpha()
        self.bear_frame5 = pygame.image.load('Frames/Bear_0005.png').convert_alpha()
        self.sprites = [self.bear_frame0, self.bear_frame1,self.bear_frame2, self.bear_frame3, self.bear_frame4, self.bear_frame5, self.bear_frame4,
                       self.bear_frame2,self.bear_frame1]
        self.current_sprite = 0
        #dead
        self.death_animation_timer = 0
        self.clock = clock
        #load it up
        self.image = self.bear_frame0
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, 435))
    def move(self):
        self.x += self.speed
    def walking(self):
        self.is_walking = True
    def hurt_animate(self):
        animation_frames = len(self.atksprites)
        frame_duration = 1000  # Time in milliseconds
        start_time = pygame.time.get_ticks()

        for frame in range(animation_frames):
            elapsed_time = pygame.time.get_ticks() - start_time
            if elapsed_time >= frame * frame_duration:
                print(self.current_atk)
                print(animation_frames - 1)
                self.image = self.atksprites[self.current_atk]

                if self.current_atk == animation_frames - 1:
                    self.current_atk = 0
                    break
                self.current_atk += 1
            pygame.display.update()

    def hurt(self, tower, whales):
        self.current_atk += .2 #1/5th of a second switch frames
        if self.current_atk >= len(self.atksprites): #7 frames, 63/60 seconds for entire animation to play out
            self.current_atk = 0
        self.image = self.atksprites[int(self.current_atk)]

        #whale getting hurt
        if self.atkspeed > 60: #attacking every second
            if self.atktower == True:
                if tower.sprite.health > 0:
                    tower.sprite.health -= 5
            elif self.atkunit == True:
                if whales.sprites():
                    whales.sprites()[0].health -= 5
            self.atkspeed = 0
        self.atkspeed += 1
    def death(self,viewport_x):
        self.is_walking = False
        frame = 300
        self.death_animation_timer += self.clock.get_time()
        self.image = self.deadsprite
        self.speed = -8
        if self.death_animation_timer >= frame:
            self.death_animation_timer = 0
            self.kill()

    def update(self,viewport_x,tower, whales):
        if self.is_walking:
            self.current_sprite += 0.12 #9/60th of a second
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]
        else: self.current_sprite = 0

        self.viewport_x = viewport_x
        self.move()
        self.rect = self.image.get_rect(topleft=(self.x-self.viewport_x, 435))

        if self.atktower or self.atkunit:
            self.is_walking = False
            #self.hurt_animate()
            self.hurt(tower, whales)
        else:
            self.is_walking = True
            self.current_atk = 0

        text = font.render(str(self.health) + " / " + str(self.maxhealth), True, (255, 255, 255))
        text_rect = self.image.get_rect(topleft=(self.x + self.width / 10 - viewport_x, 300))
        window.blit(text, text_rect)
        if self.health <= 0:
            self.death(viewport_x)
