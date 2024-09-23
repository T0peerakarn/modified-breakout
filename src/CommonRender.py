from src.constants import *
from src.resources import *
import pygame

def RenderScore(screen, score):
    small_font = pygame.font.Font('./fonts/font.ttf', 24)
    t_score = small_font.render(f"Score: {score}", False, (255, 255, 255))
    screen.blit(t_score, (8, HEIGHT - 24 - 4))

def RenderHealth(screen, health):
    x_pos = WIDTH - 111
    for i in range(health):
        screen.blit(sprite_collection["heart"].image, (x_pos, HEIGHT - 33 - 4))
        x_pos += 33

    for i in range(3-health):
        screen.blit(sprite_collection["empty_heart"].image, (x_pos, HEIGHT - 33 - 4))
        x_pos += 33
