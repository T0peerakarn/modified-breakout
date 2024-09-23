import pygame
from src.constants import *
from src.Dependency import *

class Item:
  def __init__(self, itemType, x, y, dy):
    
    self.itemType = itemType
    
    self.width = 32
    self.height = 32

    self.rect = pygame.Rect(x, y, self.width, self.height)

    self.dy = dy

  def update(self, dt):
    if self.rect.y <= HEIGHT:
      self.rect.y += self.dy * dt
  
  def Collides(self, target):
    if self.rect.x > target.rect.x + target.width or target.rect.x >self.rect.x + self.width:
      return False

    if self.rect.y > target.rect.y + target.height or target.rect.y > self.rect.y + self.height:
      return False

    return True
  
  def render(self, screen):
    screen.blit(items_image_list[self.itemType], (self.rect.x, self.rect.y))
