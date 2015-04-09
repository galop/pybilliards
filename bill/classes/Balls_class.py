from env_variables import *
from math import *
import pygame
import random

class Balls:
    def __init__(self, (x,y), size, thickness=0, color=(0,0,255), pocket_size = 0):
        self.x = x
        self.y = y
        self.size = size
        self.thickness = thickness              # Default :D
        self.color = color
        self.c1 = color[0]
        self.c2 = color[1]
        self.c3 = color[2]
        self.speed = 1
        self.angle = 0   
        self.dist = 0                        # This is in radian :D
        if pocket_size == 0:
            pocket_size = 2*self.size

        self.pocket_size = pocket_size

        self.pocketed = self.is_pocketed(self.pocket_size)      # Dpending on its initialization location :D
        self.in_line_with_white_ball = 0        # Default is zero, but will be changed afterwards :D
        self.ok_to_hit = 0                      # This will be made equal to 1 for white_ball in line with this ball

    def disp(self):
        pygame.draw.circle(gameDisplay, self.color, (self.x, self.y), self.size, self.thickness)
        pygame.display.update()

    def boundary(self):
        if self.x > dispWidth - self.size:
            self.x = 2*(dispWidth - self.size) - self.x
            self.angle = - self.angle

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle

        if self.y > dispHeight - self.size:
            self.y = 2*(dispHeight - self.size) - self.y
            self.angle = pi - self.angle

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = pi - self.angle


    def move(self, dist, angle, speed, smear=False):
        self.angle = angle
        self.speed = speed

        # Adding boundary function :D
        # s = "current distance of movement is " + str(dist)
        # msg2screen(s,self.x - 100, self.y + 200)
        while dist > 0:
            # s = "current distance of movement is " + str(dist)
            # msg2screen(s,self.x - 100, self.y + 200)
            if not smear:
                gameDisplay.fill(GREEN)

            self.x += int(round(sin(self.angle) * self.speed))
            self.y -= int(round(cos(self.angle) * self.speed))

            #---------
            self.boundary()
            #---------

            # if (self.x + self.size) > dispWidth or (self.x - self.size) < 0 or (self.y + self.size) > dispHeight or (self.y - self.size)< 0:
            #     s = "I am breaking it bad .... :( " + str(dist)
            #     msg2screen(s,self.x - 100, self.y + 200)
            #     pygame.display.update()
            #     break
            # else:
            #     s = "I am doing it good .... :) " + str(dist)
            #     msg2screen(s,self.x - 100, self.y + 200)
            #     pygame.display.update()

            self.disp()
            # pygame.display.update()
            dist -= 1 # Movement of these units only :D
        # s = "current distance of movement is " + str(dist)
        # msg2screen(s,self.x - 100, self.y + 200)
    def move_with_collision_detection(self,dist = None, angle = None, list_of_ball_objects = [], speed = 3, smear = False):
        # NOTE: 
        # This is specially used for the ball_point tracing :D
        # Find the related code in trace_for_white_ball :D

        # This variable is to detect the journey of ball_point
        # If during its journey is is pocketed then, I will return 1, hence the white_ball
        # can hit the shot, and ball will be pocketed :D
        in_journey = 0

        if dist != None:
            self.dist = dist

        if angle != None:
            self.angle = angle

        if list_of_ball_objects == []:
            list_of_ball_objects.append(self)
        
        self.speed = speed

        while self.dist > 0 & (self.pocketed == 0):
            # s = "current distance of movement is " + str(dist)
            # msg2screen(s,self.x - 100, self.y + 200)
            if not smear:
                gameDisplay.fill(GREEN)

            self.x += int(round(sin(self.angle) * self.speed))
            self.y -= int(round(cos(self.angle) * self.speed))
            
            p, q = self.x + 10, self.y + 10
            s = str(self.dist)
            msg2screen(s,p,q)
            #---------
            self.collision_detection(list_of_ball_objects, self.dist)

            temp_ball_for_pocket_size = list_of_ball_objects[0]

            temp = self.is_pocketed(temp_ball_for_pocket_size.pocket_size)

            if temp == 1:
                in_journey = 1
                self.dist = 0       # If the ball_point is pocketed, then no more distance to move for it :D
            else:
                self.boundary()
                #---------
            self.disp()
            pygame.display.update()
            self.dist -= 1 # Movement of these units only :D
        
        return in_journey

    def move_with_collision_correction(self,dist = None, angle = None, speed = None, list_of_ball_objects = []):
        
        if dist != None:
            self.dist = dist

        if angle != None:
            self.angle = angle

        if list_of_ball_objects == []:
            list_of_ball_objects.append(self)
        
        if speed != None:
            self.speed = speed

        # Adding boundary function :D

        # s = "current distance of movement is " + str(dist)
        # msg2screen(s,self.x - 100, self.y + 200)
        while self.dist > 0:
            # s = "current distance of movement is " + str(dist)
            # msg2screen(s,self.x - 100, self.y + 200)
            
            # gameDisplay.fill(GREEN)

            # self.x += int(round(sin(self.angle) * self.speed))
            # self.y -= int(round(cos(self.angle) * self.speed))

            # try:
            #     self.x += int(round(sin(self.angle) * self.speed))
            #     self.y -= int(round(cos(self.angle) * self.speed))
            # except TypeError:
            #     print "Self angle: " + str(self.angle) + "Self speed: " + str(self.speed) + "Type of self.speed: " + str(type(self.speed)) + "\n"
            #     gameExit = True
            #     break

            #---------
            self.collision(list_of_ball_objects, self.dist)
            self.is_pocketed(self.pocket_size)

            self.x += int(round(sin(self.angle) * self.speed))
            self.y -= int(round(cos(self.angle) * self.speed))

            self.boundary()
            #---------
            self.disp()
            # pygame.display.update()
            self.dist -= 1 # Movement of these units only :D
        # After movement of the ball, its angle should be reset to zero :D
        # This will ensure, when any other ball will hit it, then it can move in direction determined by hitting ball :D
        self.angle = 0

    def move_with_collision_correction_2(self, dist = None, angle = None, speed = None, list_of_ball_objects = []):
        
        if dist != None:
            self.dist = dist

        if angle != None:
            self.angle = angle

        if list_of_ball_objects == []:
            list_of_ball_objects.append(self)
        
        if speed != None:
            self.speed = speed

        # Adding boundary function :D

        # s = "current distance of movement is " + str(dist)
        # msg2screen(s,self.x - 100, self.y + 200)
        while self.dist > 0:
            # s = "current distance of movement is " + str(dist)
            # msg2screen(s,self.x - 100, self.y + 200)
            
            # gameDisplay.fill(GREEN)

            

            # try:
            #     self.x += int(round(sin(self.angle) * self.speed))
            #     self.y -= int(round(cos(self.angle) * self.speed))
            # except TypeError:
            #     print "Self angle: " + str(self.angle) + "Self speed: " + str(self.speed) + "Type of self.speed: " + str(type(self.speed)) + "\n"
            #     gameExit = True
            #     break

            #---------
            self.collision_2(list_of_ball_objects)
            self.is_pocketed(self.pocket_size)
            if self.pocketed == 1:
                self.dist = 0
                break

            self.x += int(round(sin(self.angle) * self.speed))
            self.y -= int(round(cos(self.angle) * self.speed))

            self.boundary()
            #---------
            self.disp()
            # pygame.display.update()
            self.dist -= 1 # Movement of these units only :D
        # After movement of the ball, its angle should be reset to zero :D
        # This will ensure, when any other ball will hit it, then it can move in direction determined by hitting ball :D
        self.angle = 0
    def is_clicked(self, a, b):
        if hypot(self.x-a, self.y-b) <= self.size:
            return 1                                # If the point (a,b) is inside the ball then return 1 :D
        else:
            return 0                                # Else return 0 :D
    
    def collision_detection(self, temp_list_of_balls, dist):
        # NOTE:
        # Here I am only changing my self parameters, without changing anyone else parameters. Why???
        # Ans:  This is used only ball_point, specially for white_ball collision tracing :D
        #       Hence, I only want the trace of ball_point after hitting. I don't want to move the balls
        #       if the ball_point trace hits them :D

        # NOTE: temp_list_of_balls does not contain "self" by default, but it has white_ball :D
        # Following step to check existence of self is for relality check :D

        all_other_except_me = [my_ball for my_ball in temp_list_of_balls if (my_ball != self) & (my_ball.pocketed == 0)]
        print "in collision_detection no. of balls came is " + str(len(all_other_except_me))
        # This is list of all balls except me, which are not pocketed :D

        for my_ball in all_other_except_me:
            dx = my_ball.x - self.x
            dy = my_ball.y - self.y

            dist_of_separation = hypot(dx,dy)

            if dist_of_separation < (self.size + my_ball.size):             # Collision happened :D
                print "Bang Bang !! in collision detection"
                
                tangent = atan2(dy, dx)
                self.angle      = 2*tangent - self.angle
                self.dist       = self.dist/2

                

    def collision(self, all_balls, dist):
        all_other_except_me = [my_ball for my_ball in all_balls if (my_ball != self) & (my_ball.pocketed == 0)]
        # This is list of all balls except me, which are not pocketed :D

        for my_ball in all_other_except_me:
            dx = my_ball.x - self.x
            dy = my_ball.y - self.y

            dist_of_separation = hypot(dx,dy)

            if dist_of_separation < (self.size + my_ball.size):             # Collision happened :D
                print "Bang Bang !!"
                
                tangent = atan2(dy, dx)
                self.angle      = 2*tangent - self.angle
                self.dist       = self.dist/2

                my_ball.angle   = 2*tangent - my_ball.angle
                my_ball.dist    = self.dist             # This is modified distance, which 1/2 of the previous :D

                # list_for_my_ball = [temp_ball for temp_ball in all_balls if temp_ball != my_ball]

                my_ball.move_with_collision_correction(list_of_ball_objects = all_balls)

    def collision_2(self, all_balls):
        all_other_except_me = [my_ball for my_ball in all_balls if (my_ball != self) & (my_ball.pocketed == 0)]
        # This is list of all balls except me, which are not pocketed :D

        for my_ball in all_other_except_me:
            dx = my_ball.x - self.x
            dy = my_ball.y - self.y

            dist_of_separation = hypot(dx,dy)

            if dist_of_separation < (self.size + my_ball.size):             # Collision happened :D
                print "Bang Bang !!"
                
                tangent = atan2(dy, dx)
                self.angle      = 2*tangent - self.angle
                self.dist       = self.dist/2

                my_ball.angle   = 2*tangent - my_ball.angle
                my_ball.dist    = self.dist             # This is modified distance, which 1/2 of the previous :D

                # list_for_my_ball = [temp_ball for temp_ball in all_balls if temp_ball != my_ball]

    def is_pocketed(self, pocket_size):
        x_limits = (0, dispWidth/2, dispWidth)
        y_limits = (0, dispHeight)

        for i in x_limits:
            for j in y_limits:
                ball_dist = hypot(self.x - i, self.y -j)
                if ball_dist < pocket_size:
                    self.pocketed = 1
                    self.dist = 0           # So that the ball will not move any further :D
                    return 1
        return 0

def move_my_all_balls(list_of_balls):
    dist_sum_vect = [a_ball.dist for a_ball in list_of_balls]
    dist_sum = sum(dist_sum_vect)
    while dist_sum > 0:
        for moving_ball in list_of_balls:
            # Here I am moving all balls :D
            # All those balls have distance of movement = 0, will mot move :D
            if moving_ball.dist > 0:
                moving_ball.move_with_collision_correction_2(dist = moving_ball.dist, angle = moving_ball.angle, speed = 2, list_of_ball_objects = list_of_balls)

        dist_sum_vect = [a_ball.dist for a_ball in list_of_balls]
        dist_sum = sum(dist_sum_vect)

