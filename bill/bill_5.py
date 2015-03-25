#!/usr/bin/python
# Slope problem is solved
# Slope controlled
# 
import pygame

# import time
import random
from math import *
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
FPS = 40
dispHeight = 600
dispWidth = 800
font = pygame.font.SysFont(None, 25)

gameDisplay = pygame.display.set_mode((dispHeight,dispWidth))
pygame.display.set_caption('theVault')
clock = pygame.time.Clock()

pygame.display.update()


def msg2screen(msg, x_loc=dispWidth/4, y_loc=dispHeight/2, color=black):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [x_loc,  y_loc])


def stick(block_size, stickList): # This will print our stick of finite length :D
    for each in stickList:
        pygame.draw.rect(gameDisplay, blue, [each[0], each[1], block_size, block_size])

def get_points(x1,y1,x2,y2,curr_dist,m,choice):
    # choice = 0 for start point , 
    #        = 1 for end point :D

    # In logic, (x1,y1) is start point, and (x2,y2) is end point
    # What I am finding out it another point on the line at distance "curr_dist" in direction of movement :D

    # if (y2 >= y1) ^ choice:
    # # y2 = y2-1
    #     y = y1 - curr_dist
    # else:
    # # y2 = y2+1
    #     y = y1 + curr_dist

    # x = x2 + round(m*(y - y2))  # From (x2,y2) and y selected, x will be found out :D
    a = dispWidth/4
    b = 3*dispHeight/4

    if abs(y2-y1) >= abs(x2-x1):
        if (y2 >= y1) ^ choice:
        # y2 = y2-1
            y = y1 - curr_dist
        else:
        # y2 = y2+1
            y = y1 + curr_dist

        x = x2 + round(m*(y - y2))  # From (x2,y2) and y selected, x will be found out :D
        s = "<<--------Inside y------->>  " + str(m)
    else:
        if (x2 >= x1) ^ choice:
            x = x1 - curr_dist
        else:
            x = x1 + curr_dist

        y = y2 + round(m*(x - x2))  # From (x2,y2) and y selected, x will be found out :D
        s = "<<--------Inside x------->>  " + str(m)

    msg2screen(s,a,b)
    return (x,y)

def gameLoop():
    lead_x = dispWidth/2
    lead_y = dispHeight/2
    lead_x_del = 0
    lead_y_del = 0
    block_size = 10
    gameExit = False
    gameOver = False
    stickLength = 200
    stickList = []
    prev_key = 0        # This is initialisation before the using in program :D
    once = 0

    randAppleX = round(random.randrange(0, dispWidth - block_size)/10.0)*10
    randAppleY = round(random.randrange(0, dispHeight - block_size)/10.0)*10

    stick_loc = []

    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    screen = pygame.display.set_mode((dispHeight, dispWidth), 0, 32)
    while not gameExit:
        print "General loop :D"
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

                mods = pygame.key.get_mods()        # Assining a name, to use easily :D

                        
                if event.key == pygame.K_q:
                    gameOver = True
                # elif event.key == pygame.K_RCTRL: # This is for special R_CTRL key :D
                #     print "Inside the K_RCTRL loop :D"
                    
                
        

        # I want to remove the border overloading problem. i.e. game should run even
        # after the stick crosses it. :D
        # stick will just come from other side, after it crosses the boundary :D




        gameDisplay.fill(white)

        mouse_pos = pygame.mouse.get_pos()

        # for x in xrange(0,640,20):
        #     pygame.draw.line(screen, (0, 0, 0), (x, 0), mouse_pos)              # (x,0) is start point and mouse_pos is end point :D
        #     pygame.draw.line(screen, (0, 0, 0), (x, 479), mouse_pos)

        # for y in xrange(0,480,20):
        #     pygame.draw.line(screen, (0, 0, 0), (0, y), mouse_pos)
        #     pygame.draw.line(screen, (0, 0, 0), (639, y), mouse_pos)
         # pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, block_size, block_size])
        
        print "mouse location", mouse_pos
        # x = round(random.randrange(0, dispWidth - block_size)/10.0)*10
        mouse_butt = pygame.mouse.get_pressed()
        
        #---------------
        # if mouse_butt[0] == 1:
        #     s = "left and right clicked "
        #     if mouse_butt[2]==0:
        #         s = "left pressed buttttttt right not clicked"
        #         msg2screen(s)
        #         pygame.display.update()
        #         pass
        #     msg2screen(s)
        #     pygame.display.update()
        # else:
        #     s = "left not pressed"
        #     msg2screen(s)
        #     pygame.display.update()
        #---------------
        
        # stick_loc = []
        if mouse_butt[0] == 1:

            # This logic is for saving the start point of stick :D
            # Otherwise its not possible to store the initial value of mouse_position :D
            temp = pygame.mouse.get_pos()
            stick_loc.append(temp)

            
            # if mouse_butt[2]==0:
            #     pass
            #--------------------------------------------------------------------
            mouse_pos = pygame.mouse.get_pos()
            
            x2 = mouse_pos[0] # First coordinate is x-cordinate :D
            y2 = mouse_pos[1]

            start_point = stick_loc[0]   # Here I am getting the start point value :D

            x1 = start_point[0]
            y1 = start_point[1]

            # slope of the line
            # m = float((y2-y1))/(x2-x1)              #          (y2-y1)
                                    #                (y-y1) =  ------- * (x-x1)                                      
                                               #               (x2-x1) 
            # c = y1 - m*x1 # This is constant 

            # This checking for the distance between the two points greater than or less than the stickLength :D
            hamming_dist = sqrt((y2-y1)**2+(x2-x1)**2)   
            while (hamming_dist > stickLength):
                if abs(y2-y1) > abs(x2-x1):             # If the y side distnace is greater :D, so I will find point in that direction :D
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

            end_point = (x2,y2)    # This is point that has been founf out successfully :D
            # (x,0) is start point and mouse_pos is end point :D
            # Last parameter is for the width of the line :D
            pygame.draw.line(screen, (0, 0, 0), start_point, end_point,10)           # This pretty bad line, no smppthness
            pygame.draw.aaline(screen, (0, 0, 0), start_point, end_point,30)
            
            pygame.draw.arc(screen, (255, 0, 0), ((100, 100), (200, 200)), 0, pi, 1)              
            mouse_butt = pygame.mouse.get_pressed()
            print "mouse status", mouse_butt

            # This will move the stick if first button i.e. left is clicked
            # Distance of movement of stick will be given by the location of mouse from end of stick
            # Why?
            # This is kind of velocity thing
            # Farther the mouse more distance the stick will cover :D
            # NOTE: Stick will not cross the boundary of pool table :D
            pygame.display.update()                 
            #--------------------------------------------------------------------
        # Thought:
        # left click:       Fix the stick start point
        # middle click:     undo of left click and hang there freely
        # right click:      Hit the stick :D, and hang there freely

        
        # if mouse_butt[0] == 1:
        #     s = "only left"
        #     while (True):
        #         mouse_butt = pygame.mouse.get_pressed()
        #         if mouse_butt[1] == 1:
        #             s = "left -> middle"
        #             break
        #         elif mouse_butt[2] == 1:
        #             s = "left -> right"
        #             break
        #         break



            if mouse_butt[2] == 1 : # & mouse_butt[0] == 0:
                
                x3 = mouse_pos[0] # First coordinate is x-cordinate :D
                y3 = mouse_pos[1]

                # x2,y2 are endpoint co-ordinates :D

                # Movement distance :D
                move_dist = sqrt((y2-y3)**2+(x2-x3)**2)

                # if (x2-x1)!=0:
                #     m1 = float(y2-y1)/(x2-x1)
                #     print "in y", m1

                # if (y2-y1)!=0:
                #     m2 = float(x2-x1)/(y2-y1)
                #     print "in x", m2

                curr_dist = 1   # This is current distance achieved :D
                out_msg = "Moving distance is "  + str(move_dist)
                msg2screen(out_msg,dispWidth/4,dispHeight/4)

                while (start_point[0] > 0) & (start_point[0] < dispWidth) & (start_point[1] > 0) & (start_point[1] < dispHeight) & (curr_dist < move_dist):
                    # hamming_dist = sqrt((y2-y1)**2+(x2-x1)**2)   
                    

                    
                        

                    if (x2-x1)!=0:
                                                    #          (y2-y1)
                                    #                (y-y1) =  ------- * (x-x1)                                      
                                               #               (x2-x1) 
                        m1 = float(y2-y1)/(x2-x1)
                        m = m1

                    elif (y2-y1)!=0:
                                                    #          (x2-x1)
                                    #                (x-x1) =  ------- * (y-y1)                                      
                                               #               (y2-y1)                     
                        m2 = float(x2-x1)/(y2-y1)
                        m = m2
                    
                    if abs(m)>1:
                        m = 1/m

                    # -------------------------
                    # Note down the ordering of elements :D
                    start_point = get_points(x1,y1,x2,y2,curr_dist,m,0)         # choice = 0, for start point
                    end_point = get_points(x2,y2,x1,y1,curr_dist,m,1)           # choice = 1, for end point

                    curr_dist += 1

                    

                    
                    # Last parameter is for the width of the line :D
                    pygame.draw.line(screen, (255, 0, 0), start_point, end_point,20)           # This pretty bad line, no smppthness
                    pygame.display.update()
        
        else:
            # This is like whenever I am not holding the stick to initialise,
            # clear the points in that :D
            stick_loc = []
        
        
        clock.tick(FPS)
        s = "Length of stick_loc is: "+ str(len(stick_loc))
        msg2screen(s)
        pygame.display.update()

    pygame.quit()
    print "++++-----------------------------------++++"
    quit()

gameLoop()
