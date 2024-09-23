import pygame
import random
from src.constants import *
from src.Item import *

class Brick:
    def __init__(self, x, y):
        self.tier=0   #n->0
        self.color=1  #5->1

        self.x=x
        self.y=y

        self.width = 96
        self.height = 48

        self.alive = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if random.uniform(0, 1) < 0.2:
            if random.uniform(0, 1) < 0.9:
                self.reward = Item(ITEM_MULTIPLE, self.x + 48 - 16, self.y + 24 - 16, 100)
            else:
                self.reward = Item(ITEM_HEART, self.x + 48 - 16, self.y + 24 - 16, 100)
        else:
            self.reward = None
        

    def Hit(self):
        gSounds['brick-hit2'].play()

        if self.tier > 0:
            if self.color == 1:
                self.tier = self.tier - 1
                self.color = 5
            else:
                self.color = self.color - 1

        else:
            if self.color == 1:
                self.alive = False
            else:
                self.color = self.color - 1

        if not self.alive:
            gSounds['brick-hit1'].play()
    
    def Break(self):
        gSounds['brick-hit1'].play()
        self.alive = False

    def update(self, dt):
        if not self.alive and self.reward != None:
            self.reward.update(dt)

    def render(self, screen):
        if self.alive:
            screen.blit(brick_image_list[((self.color-1)*4)+self.tier], (self.rect.x, self.rect.y))
        elif self.reward != None:
            self.reward.render(screen)