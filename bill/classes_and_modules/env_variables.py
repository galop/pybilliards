ADV_MODE = 1

WHITE = (255, 255, 255)

GREEN = (0, 140, 0)



FPS = 60
dispSize = dispWidth, dispHeight = 800, 600

scorecardSize = scorecardWidth, scorecardHeight = 400, 100
cue_limit = 20
default_speed = 5
no_of_balls = 6  # 3
my_ball_size = 14   # 25
my_pocket_size = 2*my_ball_size

import pygame
# import random
from math import *
pygame.init()

font = pygame.font.SysFont(None, 25)
gameDisplay = pygame.display.set_mode(dispSize)
# scoreDisplay = pygame.display.set_mode(scorecardSize)
pygame.display.set_caption('pyBilliard')
clock = pygame.time.Clock()

YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
DARK_GREEN = (0, 255, 0)
MAROON = (128, 0, 0)
BLACK = (0, 0, 0)

ball_num_col_dict = {1:YELLOW, 2:BLUE, 3:RED, 4:PURPLE, 5:ORANGE, 6:DARK_GREEN, 7:MAROON, 8:BLACK}

ball_loc = {}
a, b = dispSize

proc_balls = 1
hori_disp = 2*my_ball_size*cos(pi/6)

str_loc_placing = int(3*a/4)

for i in xrange(1, int(sqrt(2*no_of_balls)) + 2) :
	this_level_top_ball_centre = int(b/2) + (i-1)*my_ball_size

	t_x = str_loc_placing + (i-1)*hori_disp # Common to all balls at same level

	for j in xrange(proc_balls, proc_balls+i):
		if j > no_of_balls:
			break
		# print j
		
		t_y = this_level_top_ball_centre - 2*(j - proc_balls)*my_ball_size
		ball_loc[j] = (t_x, t_y)
	proc_balls += i