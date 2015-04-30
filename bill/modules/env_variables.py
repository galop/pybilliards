# Hardik
import pygame
from math import *

ADV_MODE = 1
RAND_MODE = 0

# ini_score = {"Shots": 0, "Pocketed": 0}
# game_score = {1:{"Shots": 0, "Pocketed": 0}, 2:{"Shots": 0, "Pocketed": 0}, 3:{"Shots": 0, "Pocketed": 0}}
# 1: User 1, 2: User 2, 3: Computer

WHITE = (255, 255, 255)
GREEN = (0, 140, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
DARK_GREEN = (0, 255, 0)
MAROON = (128, 0, 0)
BLACK = (0, 0, 0)
SCORECARDCOLOR = (225, 145, 45)

FPS = 60
dispSize = dispWidth, dispHeight = 800, 500
TITLE = "pyBilliards"
cue_limit = 20
default_speed = 5
no_of_balls = 8  # 3
my_ball_size = 14   # 25
my_pocket_size = 2*my_ball_size

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
font = pygame.font.SysFont("ubuntu", 34)
gameDisplay = pygame.display.set_mode(dispSize)  # 1
tempTable = pygame.Surface(dispSize)
tempTable.fill(GREEN)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
hit = pygame.mixer.Sound("assets/wood17.aif")
inpocketsound = pygame.mixer.Sound("assets/inpocket.aif")

SOUNDS = True

ball_num_col_dict = {1: YELLOW,
                     2: BLUE,
                     3: RED,
                     4: PURPLE,
                     5: ORANGE,
                     6: DARK_GREEN,
                     7: MAROON,
                     8: BLACK
                     }

ball_loc = {}
a, b = dispSize

proc_balls = 1
hori_disp = 2*(my_ball_size + 2)*cos(pi/6)

str_loc_placing = int(3*a/4)

for i in xrange(1, int(sqrt(2*no_of_balls)) + 2):
    this_level_top_ball_centre = int(b/2) + (i-1)*(my_ball_size+1)

    t_x = str_loc_placing + (i-1)*hori_disp  # Common to all balls at same level

    for j in xrange(proc_balls, proc_balls+i):
        if j > no_of_balls:
            break

        t_y = this_level_top_ball_centre - (2*(j-proc_balls)*(my_ball_size+1))
        ball_loc[j] = (t_x, t_y)
    proc_balls += i
