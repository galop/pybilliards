white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
GREEN = (0,140,0)
FPS = 100
dispHeight = 500
dispWidth = 800

no_of_balls = 3    # 3
my_ball_size = 20   # 25

import pygame
import random
from math import *
pygame.init()

font = pygame.font.SysFont(None, 25)
gameDisplay = pygame.display.set_mode((dispWidth, dispHeight))
pygame.display.set_caption('pyBilliard')
clock = pygame.time.Clock()