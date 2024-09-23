import pygame
from src.constants import *
from src.Dependency import *

class Ball:
    def __init__(self, initial_skin, x=WIDTH/2-6, y=HEIGHT/2-6, dx=0, dy=0, speed_multiplier = 1):
        self.width = 24
        self.height = 24

        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.speed_multiplier = speed_multiplier
        self.dx = dx
        self.dy = dy

        self.initial_skin = initial_skin
        self.image = ball_image_list[initial_skin]
        #self.rect = pygame.Rect(self.x, self.y, self.width, self.height)



    def Collides(self, target):
        if self.rect.x > target.rect.x + target.width or target.rect.x >self.rect.x + self.width:
            return False

        if self.rect.y > target.rect.y + target.height or target.rect.y > self.rect.y + self.height:
            return False

        return True

    def Reset(self):
        self.x = WIDTH/2 - 6
        self.y = HEIGHT/2 - 6
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.dx = 0
        self.dy = 0


    def update(self, dt):
        self.rect.x += self.dx * dt * self.speed_multiplier
        self.rect.y += self.dy * dt * self.speed_multiplier
        
        if self.speed_multiplier > 1:
            self.speed_multiplier -= 0.01
            
        #A ball hits a left wall
        if self.rect.x <= 0:
            self.rect.x = 0
            self.dx = -self.dx
            gSounds['wall-hit'].play()

        # A ball hits a right wall
        if self.rect.x >= WIDTH - 24:
            self.rect.x = WIDTH - 24
            self.dx = -self.dx
            gSounds['wall-hit'].play()

        # A ball hits a upper wall
        if self.rect.y <= 0:
            self.rect.y = 0
            self.dy = -self.dy
            gSounds['wall-hit'].play()

    def render(self, screen):
        # rect.x rect.y is center?? or is it square box
        # rect = self.image.get_rect()
        # rect.center = (self.rect.x, self.rect.y)
        screen.blit(self.image, (self.rect.x, self.rect.y))
