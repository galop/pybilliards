#!/usr/bin/python
# This file is based on stick py file namely "fourth_rvg.py" designed in previous folder.
# This features simple apple to pushed by the stick
# stick will be given some finite length, now on we will call it a stick and apple as ball 
# So ball will also have some finite size, resolution is to be increased, to incorporate smooth transitions
# After stick hits the ball, it will move by some constant amount of distance. (why not variable? Beacuse that will
# be incorporated in next file ) Currently only finite distance, and finite constant velocity of the stick 

import pygame
# import time
import random
from math import *
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
FPS = 20
dispHeight = 600
dispWidth = 600
font = pygame.font.SysFont(None, 25)

gameDisplay = pygame.display.set_mode((dispHeight, dispWidth))
pygame.display.set_caption('Billiards')
clock = pygame.time.Clock()

pygame.display.update()


def msg2screen(msg, color=black):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [dispWidth/2,  dispHeight/2])


def stick(block_size, stickList): # This will print our stick of finite length 
    for each in stickList:
        pygame.draw.rect(gameDisplay, blue, [each[0], each[1], block_size, block_size])


def gameLoop():
    # lead_x = dispWidth/2
    # lead_y = dispHeight/2
    # lead_x_del = 0
    # lead_y_del = 0
    # block_size = 10
    gameExit = False
    gameOver = False
    stickLength = 400
    # stickList = []
    # prev_key = 0        # This is initialisation before the using in program 
    # once = 0

    # randAppleX = round(random.randrange(0, dispWidth - block_size)/10.0)*10
    # randAppleY = round(random.randrange(0, dispHeight - block_size)/10.0)*10

    # print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    screen = pygame.display.set_mode((dispHeight, dispWidth), 0, 32)
    while not gameExit:
        # print "General loop "
        while gameOver:
            gameDisplay.fill(white)
            msg2screen("Game over, press Q to quit or C to continue.")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:

                mods = pygame.key.get_mods()        # Assining a name, to use easily 
                        
                if event.key == pygame.K_q:
                    gameOver = True
                # elif event.key == pygame.K_RCTRL: # This is for special R_CTRL key 
                #     print "Inside the K_RCTRL loop "
                    
                
        # I want to remove the border overloading problem. i.e. game should run even
        # after the stick crosses it. 
        # stick will just come from other side, after it crosses the boundary 


        gameDisplay.fill(white)

        mouse_pos = pygame.mouse.get_pos()

        # print "mouse location", mouse_pos
        # x = round(random.randrange(0, dispWidth - block_size)/10.0)*10
        start_point = (30,60)
        

        # slope of the line
        x2 = mouse_pos[0] # First coordinate is x-cordinate 
        y2 = mouse_pos[1]
        x1 = start_point[0]
        y1 = start_point[1]

        # m = float((y2-y1))/(x2-x1)              #          (y2-y1)
        #                         #                (y-y1) =  ------- * (x-x1)                                      
        #                                    #               (x2-x1) 
        # c = y1 - m*x1 # This is constant 

        # This checking for the distance between the two points greater than or less than the stickLength 
        hamming_dist = sqrt((y2-y1)**2+(x2-x1)**2)   
        while (hamming_dist > stickLength):
            if abs(y2-y1) > abs(x2-x1):             # If the y side distnace is greater , so I will find point in that direction 
                if y2 > y1:
                    y2 = y2-1
                else:
                    y2 = y2+1
            else:
                if x2 > x1:
                    x2 = x2-1
                else:
                    x2 = x2+1

            hamming_dist = sqrt((y2-y1)**2+(x2-x1)**2) 

        end_point = (x2,y2)    # This is point that has been founf out successfully 
        pygame.draw.aaline(screen, (0, 0, 0), start_point, end_point)              # (x,0) is start point and mouse_pos is end point 


        
        pygame.display.update()

        
        
        clock.tick(FPS)
    pygame.quit()
    quit()

gameLoop()
