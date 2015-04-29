from env_variables import *
from math import *
import pygame
import random
import sys
# sys.path.append(r'/Documents/Python_2015/pybilliards/bill/modules/')
# from all_functions import *
# from all_functions import *


class Balls:
    def __init__(self, (x, y), size=20, thickness=0, color=(0, 0, 255), pocket_size=0, angle=0, number=0, speed=0):
        self.x = int(x)
        self.y = int(y)
        self.size = int(size)
        self.thickness = int(thickness)              # Default :D
        self.color = color
        self.c1 = color[0]
        self.c2 = color[1]
        self.c3 = color[2]
        self.speed = speed
        self.angle = angle
        self.dist = 0                        # This is in radian :D
        if pocket_size == 0:
            pocket_size = 2*self.size

        self.pocket_size = pocket_size

        self.pocketed = self.is_pocketed(self.pocket_size)      # Dpending on its initialization location :D
        self.in_line_with_white_ball = 0        # Default is zero, but will be changed afterwards :D
        self.ok_to_hit = 0                      # This will be made equal to 1 for white_ball in line with this ball
        self.correction_angle = 0
        self.number = number
        self.offset_speed = 0
        self.default_speed = 2

    def disp(self):
        gameDisplay.blit(Balls.shadow_img, (self.x - 14, self.y - 14))
        pygame.draw.circle(gameDisplay, self.color, (self.x, self.y), self.size, self.thickness)
        gameDisplay.blit(Balls.shading_img, (self.x - 15, self.y - 15))
        # pygame.display.update()

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
        while dist > 0:
            # s = "current distance of movement is " + str(dist)
            # msg2screen(s,self.x - 100, self.y + 200)
            if not smear:
                gameDisplay.fill(GREEN)

            x_change = int(round(sin(self.angle) * self.speed))
            y_change = int(round(cos(self.angle) * self.speed))

            self.x += x_change
            self.y -= y_change
            self.boundary()
            self.disp()
            # pygame.display.update()
            dist -= hypot(x_change, y_change)  # Movement of these units only :D
        # s = "current distance of movement is " + str(dist)
        # msg2screen(s,self.x - 100, self.y + 200)


    def move_with_collision_correction_2_rotation(self, dist = None, angle = None, speed = None, list_of_ball_objects = [], smear = False, show_me = False, ball_will_got_hit = None):
        if dist is not None:
            self.dist = dist
        if angle is not None:
            self.angle = angle
        if list_of_ball_objects == []:
            list_of_ball_objects.append(self)
        if speed is not None:
            self.speed = speed
        while self.dist > 0:
            for a_ball in list_of_ball_objects:
                a_ball.disp()
            if not smear:
                gameDisplay.fill(GREEN)
            # try:
            #     self.x += int(round(sin(self.angle) * self.speed))
            #     self.y -= int(round(cos(self.angle) * self.speed))
            # except TypeError:
            #     print "Self angle: " + str(self.angle) + "Self speed: " + str(self.speed) + "Type of self.speed: " + str(type(self.speed)) + "\n"
            #     gameExit = True
            #     break

            #---------
            self.rotate_collision_2(list_of_ball_objects, ball_will_got_hit)
            self.is_pocketed(self.pocket_size)

            if self.pocketed == 1:
                self.dist = 0
                break

            self.x += int(round(sin(self.angle) * self.speed))
            self.y -= int(round(cos(self.angle) * self.speed))

            self.boundary()
            #---------
            if show_me == True: 
                self.disp()
            # pygame.display.update()
            # print str(self) + "dist inside the corr_2: " + str(self.dist)
            self.dist -= 1 # Movement of these units only :D
        # After movement of the ball, its angle should be reset to zero :D
        # This will ensure, when any other ball will hit it, then it can move in direction determined by hitting ball :D
        self.angle = 0

    def move_with_collision_detection(self,  dist=None, angle=None,list_of_ball_objects=[], speed=3, smear=False, show_me=True):
        from all_functions import *
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
                # gameDisplay.fill(GREEN)
                show_table()

            x_change = int(round(sin(self.angle) * self.speed))
            y_change = int(round(cos(self.angle) * self.speed))

            self.x += x_change
            self.y -= y_change

            self.collision_detection(list_of_ball_objects, self.dist)

            temp_ball_for_pocket_size = list_of_ball_objects[0]

            temp = self.is_pocketed(temp_ball_for_pocket_size.pocket_size)

            if temp == 1:
                in_journey = 1
                self.dist = 0       # If the ball_point is pocketed, then no more distance to move for it :D
            else:
                self.boundary()
                #---------
            if show_me == True:
                self.disp()
            pygame.display.update()
            self.dist -= hypot(x_change, y_change) # Movement of these units only :D
        
        return in_journey

    def move_with_collision_correction(self, dist = None, angle = None, speed = None, list_of_ball_objects = []):

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
            self.collision(list_of_ball_objects, self.dist)
            self.is_pocketed(self.pocket_size)

            x_change = int(round(sin(self.angle) * self.speed))
            y_change = int(round(cos(self.angle) * self.speed))

            self.x += x_change
            self.y -= y_change

            self.boundary()
            #---------
            self.disp()
            # pygame.display.update()
            self.dist -= hypot(x_change, y_change) # Movement of these units only :D
        # After movement of the ball, its angle should be reset to zero :D
        # This will ensure, when any other ball will hit it, then it can move in direction determined by hitting ball :D
        self.angle = 0

    def collision_2(self, all_balls):
        from all_functions import *
        #============
        
        
        show_table()
        # pygame.display.update()
        #============

        all_other_except_me = [my_ball for my_ball in all_balls if (my_ball != self) & (my_ball.pocketed == 0)]
        # This is list of all balls except me, which are not pocketed :D

        for my_ball in all_other_except_me:
            dx = self.x - my_ball.x
            dy = self.y - my_ball.y
            tangent = atan2(dy, dx)
            dist_of_separation = hypot(dx,dy)

            if dist_of_separation <= (self.size + my_ball.size + 2):             # Collision happened :D
                
                

                my_ball.angle = get_angle((my_ball.x, my_ball.y), self)
                dist_correction_angle = my_ball.angle - self.angle

                self.angle = 2*tangent - self.angle


                self.angle = self.angle % (2*pi)
                my_ball.angle = my_ball.angle % (2*pi)

                # This is bouncing of balls before hitting each other, so they will not be trapped inside the 
                # internal bouncing, and leanding nowhere :D
                # NOTE: THIS IS VERY IMPORTANT NEVER REMOVE THIS
                k = 10
                self.x += int(round(k*sin(self.angle)))
                self.y -= int(round(k*cos(self.angle)))
                self.boundary()

                my_ball.x += int(round(k*sin(my_ball.angle)))
                my_ball.y -= int(round(k*cos(my_ball.angle)))
                my_ball.boundary()
                # I am saving this dist_correction_angle as object parameter. This has been initialized in the __init__ of Balls class :D
                self.correction_angle = abs(dist_correction_angle*180/pi) % 360

                sine_correction = sin(abs(dist_correction_angle))
                cosine_correction = cos(abs(dist_correction_angle))

                new_self_dist = int(self.dist * sine_correction)
                new_my_ball_dist = int(self.dist * cosine_correction)

                self.dist = new_self_dist
                my_ball.dist = new_my_ball_dist

                # self.dist = self.dist / 2
                # my_ball.dist = self.dist

                #==================================================
                new_self_speed = self.speed * sine_correction
                new_my_ball_speed = self.speed * cosine_correction

                self.speed = new_self_speed
                my_ball.speed = new_my_ball_speed

                if (self.dist > 0) & (self.speed > 0):
                    self.offset_speed = float(self.speed - self.default_speed) / self.dist

                if (my_ball.dist > 0) & (my_ball.speed > 0):
                    my_ball.offset_speed = float(my_ball.speed - my_ball.default_speed) / my_ball.dist

    def move_with_collision_correction_2(self, dist=None, angle=None, speed=None, list_of_ball_objects=[], smear=False):
        if dist != None:
            self.dist = dist

        if angle != None:
            self.angle = angle

        if list_of_ball_objects == []:
            list_of_ball_objects.append(self)

        if speed != None:
            self.speed = speed

        while self.dist > 0:
            for a_ball in list_of_ball_objects:
                a_ball.disp()
            if not smear:
                gameDisplay.fill(GREEN)

            # try:
            #     self.x += int(round(sin(self.angle) * self.speed))
            #     self.y -= int(round(cos(self.angle) * self.speed))
            # except TypeError:
            #     print "Self angle: " + str(self.angle) + "Self speed: " + str(self.speed) + "Type of self.speed: " + str(type(self.speed)) + "\n"
            #     gameExit = True
            #     break

            self.collision_2(list_of_ball_objects)
            self.is_pocketed(self.pocket_size)
            if self.pocketed == 1:
                self.dist = 0
                break

            x_change = int(round(sin(self.angle) * self.speed))
            y_change = int(round(cos(self.angle) * self.speed))
            self.x += x_change
            self.y -= y_change

            self.boundary()
            self.disp()
            # pygame.display.update()
            print str(self) + "dist inside the corr_2: " + str(self.dist)
            self.dist -= hypot(x_change, y_change)  # Movement of these units only :D
        # After movement of the ball, its angle should be reset to zero :D
        # This will ensure, when any other ball will hit it, 
        # then it can move in direction determined by hitting ball :D
        self.angle = 0

    def move_with_collision_correction_3(self, dist=None, angle=None, speed=None, list_of_ball_objects=[], smear=False):
        from all_functions import *

        if dist != None:
            self.dist = dist
        if angle != None:
            self.angle = angle
        if list_of_ball_objects == []:
            list_of_ball_objects.append(self)
        if speed != None:
            self.speed = speed

        if (self.speed > 0) & (self.dist > 0):
            if not smear:
                show_table()
                # gameDisplay.fill(GREEN)

            # for a_ball in list_of_ball_objects:
            #     a_ball.disp()
            # pygame.display.update()
            #======================================
            # This shows what distance is the ball with it moves :D
            # s = "D: " + str(int(self.dist))

            # p = self.x + 20
            # q = self.y + 20
            # msg2screen(s, p, q)
            #======================================
            # try:
            #     self.x += int(round(sin(self.angle) * self.speed))
            #     self.y -= int(round(cos(self.angle) * self.speed))
            # except TypeError:
            #     print "Self angle: " + str(self.angle) + "Self speed: " + str(self.speed) + "Type of self.speed: " + str(type(self.speed)) + "\n"
            #     gameExit = True
            #     break

            #---------
            # self.collision_2(list_of_ball_objects)
            
            self.is_pocketed(self.pocket_size)
            if self.pocketed == 1:
                self.dist = 0
                self.speed = 0
            
            self.boundary()
            # This is equivalent to one time movement
            x_change = int(round(sin(self.angle) * self.speed))
            y_change = int(round(cos(self.angle) * self.speed))

            self.x += x_change
            self.y -= y_change

            self.boundary()

            self.collision_2(list_of_ball_objects)
            self.boundary()
            # self.disp()
            for a_ball in list_of_ball_objects:
                a_ball.disp()
            pygame.display.update()
            # pygame.display.update()
            # print str(self) + "dist inside the corr_2: " + str(self.dist)
            self.dist -= hypot(x_change, y_change) # Movement of these units only :D
        # After movement of the ball, its angle should be reset to zero :D
        # This will ensure, when any other ball will hit it, then it can move in direction determined by hitting ball :D
        # self.angle = 0

    def is_clicked(self, a, b):
        if hypot(self.x-a, self.y-b) <= self.size:
            return 1  # If the point (a,b) is inside the ball then return 1 :D
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
        # print "in collision_detection no. of balls came is " + str(len(all_other_except_me))
        # This is list of all balls except me, which are not pocketed :D

        for my_ball in all_other_except_me:
            dx = my_ball.x - self.x
            dy = my_ball.y - self.y

            dist_of_separation = hypot(dx, dy)

            if dist_of_separation < (self.size + my_ball.size):             # Collision happened :D
                # print "Bang Bang !! in collision detection"
                tangent = atan2(dy, dx)
                self.angle = 2*tangent - self.angle
                self.dist = self.dist/2

    def collision(self, all_balls, dist):
        all_other_except_me = [my_ball for my_ball in all_balls if (my_ball != self) & (my_ball.pocketed == 0)]
        # This is list of all balls except me, which are not pocketed :D

        for my_ball in all_other_except_me:
            dx = my_ball.x - self.x
            dy = my_ball.y - self.y

            dist_of_separation = hypot(dx, dy)

            if dist_of_separation < (self.size + my_ball.size):             # Collision happened :D
                print "Bang Bang !!"
                tangent = atan2(dy, dx)
                self.angle      = 2*tangent - self.angle
                self.dist       = self.dist/2

                my_ball.angle   = 2*tangent - my_ball.angle
                my_ball.dist    = self.dist             # This is modified distance, which 1/2 of the previous :D

                # list_for_my_ball = [temp_ball for temp_ball in all_balls if temp_ball != my_ball]

                my_ball.move_with_collision_correction(list_of_ball_objects = all_balls)

    def rotate_collision_2(self, all_balls, ball_will_got_hit):
        from all_functions import *
        #============
        my_pocket_size = 2*my_ball_size
        show_pockets(my_pocket_size)
        #============

        all_other_except_me = [my_ball for my_ball in all_balls if (my_ball != self) & (my_ball.pocketed == 0)]
        # This is list of all balls except me, which are not pocketed :D

        for my_ball in all_other_except_me:
            dx = my_ball.x - self.x
            dy = my_ball.y - self.y

            dx = -1*dx
            dy = -1*dy

            dist_of_separation = hypot(dx,dy)

            if dist_of_separation <= (self.size + my_ball.size):             
                # Collision happened :D, and I will break here only :D
                # only for first collision
                
                # By doing above assignment, I am directing all changes of the ball that got hit to
                # input ball object i.e. ball_will_got_hit

                print "Bang Bang !!"
                
                # tangent = atan2(dy, dx) + pi/2
                tangent = atan2(dy, dx)

                
                print "tangent is : " + str(tangent*180/pi)
                # By doing this the tangent will always be positive :D

                dist_correction_angle = 0

                if (self.angle > 0) & (self.angle <= pi/2):
                    # print "0-pi/2"
                    if tangent > pi/2:
                        ball_will_got_hit.angle = tangent - pi/2
                    else:
                        ball_will_got_hit.angle = tangent + 3*pi/2

                    dist_correction_angle = tangent - (self.angle - pi/2)

                    if tangent > self.angle + pi/2:
                        self.angle = ball_will_got_hit.angle - pi/2
                    else:
                        self.angle = ball_will_got_hit.angle + pi/2

                elif (self.angle > pi/2) & (self.angle <= 2*pi/2):
                    # print "pi/2-pi"
                    tangent = pi + tangent  
                    # tangent will be negative here
                    ball_will_got_hit.angle = tangent + pi/2

                    dist_correction_angle = tangent - (self.angle - pi/2)
                    if tangent > self.angle - pi/2:
                        self.angle = ball_will_got_hit.angle - pi/2
                    else:
                        self.angle = ball_will_got_hit.angle + pi/2

                elif (self.angle > 2*pi/2) & (self.angle <= 3*pi/2):
                    # print "pi-3*pi/2"
                    tangent = pi + tangent  
                    # tangent will be negative here
                    ball_will_got_hit.angle = tangent + pi/2

                    dist_correction_angle = tangent - (self.angle - pi/2)

                    # if tangent > self.angle - 2*pi/2:
                    if tangent > self.angle - pi/2:
                        self.angle = ball_will_got_hit.angle - pi/2
                    else:
                        self.angle = ball_will_got_hit.angle + pi/2

                elif ((self.angle > 3*pi/2) & (self.angle <= 4*pi/2)) or (self.angle == 0):
                    # print "3*pi/2-2*pi"
                    if tangent > pi/2:
                        ball_will_got_hit.angle = tangent - pi/2
                    else:
                        ball_will_got_hit.angle = tangent + 3*pi/2

                    dist_correction_angle = tangent - (self.angle - 3*pi/2)

                    if tangent > self.angle - 3*pi/2:
                        self.angle = ball_will_got_hit.angle - pi/2
                    else:
                        self.angle = ball_will_got_hit.angle + pi/2

                
                #=======================================
                # self.angle      = 2*tangent - self.angle
                # self.dist       = self.dist/2

                # my_ball.angle   = 2*tangent - my_ball.angle
                # my_ball.dist    = self.dist             # This is modified distance, which 1/2 of the previous :D
                #======================================
                ##
                # This is bouncing of balls before hitting each other, so they will not be trapped inside the 
                # internal bouncing, and leanding nowhere :D
                # NOTE: THIS IS VERY IMPORTANT NEVER REMOVE THIS
                self.x += int(round(10*sin(self.angle)))
                self.y -= int(round(10*cos(self.angle)))
                self.boundary()

                # my_ball.x += int(round(10*sin(my_ball.angle)))
                # my_ball.y -= int(round(10*cos(my_ball.angle)))
                # my_ball.boundary()
                
                # I am saving this dist_correction_angle as object parameter. This has been initialized in the __init__ of Balls class :D
                self.correction_angle = abs(dist_correction_angle*180/pi) %360

                sine_correction     = sin(abs(dist_correction_angle))
                # cosine_correction   = cos(abs(dist_correction_angle))

                new_self_dist       = int(self.dist * sine_correction)
                # new_my_ball_dist    = int(self.dist * cosine_correction)
                
                self.dist                   = new_self_dist
                # ball_will_got_hit.dist      = new_my_ball_dist

                #==================================================
                new_self_speed      = self.speed * sine_correction
                # new_my_ball_speed   = self.speed * cosine_correction

                self.speed      = new_self_speed
                # ball_will_got_hit.speed   = new_my_ball_speed
                #======================================
                # if my_ball.angle != 0: 
                #     # If the ball with which my_ball got hit was moving, then do this :D
                #     my_ball.angle   = 2*tangent - my_ball.angle
                #     my_ball.dist    = self.dist             # This is modified distance, which 1/2 of the previous :D
                # else my_ball.angle == 0:
                    # If my_ball hits a stationary ball then

                # list_for_my_ball = [temp_ball for temp_ball in all_balls if temp_ball != my_ball]

    def is_pocketed(self, pocket_size):
        x_limits = (0, dispWidth/2, dispWidth)
        y_limits = (0, dispHeight)

        for i in x_limits:
            for j in y_limits:
                ball_dist = hypot(self.x - i, self.y - j)
                if ball_dist < pocket_size:
                    self.pocketed = 1
                    self.dist = 0  # So that the ball will not move any further :D
                    return 1
        return 0

    def give_me_pocket_angles(self):
        # For a ball obj, this function returns a list containing movement
        # angles for all pockets

        from all_functions import *

        a = (0, dispWidth/2, dispWidth)
        b = (0, dispHeight)

        t = [] # Empty list for angles towards pockets
        for i in a:
            for j in b:
                t.append(get_angle((i,j), self))
        return t

if __name__ == "__main__":
    print "This is running individually: Balls_class"
else:
    print "This is running inside someone :d: Balls_class"