import pygame
import os

GRID_WIDTH = 5
GRID_HEIGHT = 5

CASE_SIZE = 50
CASE_BORDER = 2

FLAG_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Flag.png")), (CASE_SIZE, CASE_SIZE))
BOMB_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "Bomb.png")), (CASE_SIZE, CASE_SIZE))