from env_variables import *
from math import *
import pygame
import random as rd


class Balls:
    """ Implements snooker ball object and related methods.
    """
    def __init__(self, (x, y), size=20, thickness=0, color=(0, 0, 255), pocket_size=0, angle=0, number=0, speed=0):
        self.x = int(x)
        self.y = int(y)
        self.size = int(size)
        self.thickness = int(thickness)  # Default
        self.color = color
        self.c1 = color[0]
        self.c2 = color[1]
        self.c3 = color[2]
        self.speed = speed
        self.angle = angle  # This is in radian
        self.dist = 0
        if pocket_size == 0:
            pocket_size = 2*self.size

        self.pocket_size = pocket_size

        self.pocketed = self.is_pocketed(self.pocket_size)  # Depending initialization location
        self.in_line_with_white_ball = 0  # Default zero, but changed later
        self.ok_to_hit = 0  # 1 for white_ball in line of sight
        self.correction_angle = 0
        self.number = number
        self.offset_speed = 0
        self.default_speed = 2

    def disp(self):
        """ This function draws a circle at self locations of Ball object only if its not pocketed.
        """
        if not self.pocketed:
            tempTable.blit(Balls.shadow_img, (self.x - 14, self.y - 14))
            pygame.draw.circle(tempTable, self.color, (self.x, self.y), self.size, self.thickness)
            tempTable.blit(Balls.shading_img, (self.x - 15, self.y - 15))

    def boundary(self):
        """ Tests self location of Ball object against boundary of walls of pool table.
        """
        if self.x > dispWidth - self.size:
            self.x = 2*(dispWidth - self.size) - self.x
            self.angle = - self.angle
            self.speed = 0.97*self.speed

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle
            self.speed = 0.97*self.speed

        if self.y > dispHeight - self.size:
            self.y = 2*(dispHeight - self.size) - self.y
            self.angle = pi - self.angle
            self.speed = 0.97*self.speed

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = pi - self.angle
            self.speed = 0.97*self.speed

    def collision(self, all_balls):
        """ This function takes care of collision between Ball objects present in
            all_balls list. Each Ball object is tested against other objects, checking overlapping
            and collsiion. Respective speed and distance corrections are done for both colliding Ball
            objects. offset_speed are also changed depending on collsion or not. 
        """
        from all_functions import *
        show_table()
        all_other_except_me = [my_ball for my_ball in all_balls if (my_ball != self) & (my_ball.pocketed == 0)]
        # This is list of all balls except me, which are not pocketed :D

        for my_ball in all_other_except_me:
            dx = self.x - my_ball.x
            dy = self.y - my_ball.y
            tangent = atan2(dy, dx)
            dist_of_separation = hypot(dx, dy)

            if dist_of_separation < (self.size + my_ball.size + 2):  # Collision
                if SOUNDS:
                    hit.play()
                my_ball.angle = get_angle((my_ball.x, my_ball.y), self)
                dist_correction_angle = my_ball.angle - self.angle
                self.angle = 2*tangent - self.angle
                self.angle = self.angle % (2*pi)
                my_ball.angle = my_ball.angle % (2*pi)

                # This is bouncing of balls before hitting each other,
                # so they will not be trapped inside the
                # internal bouncing, and leanding nowhere
                # NOTE: THIS IS VERY IMPORTANT NEVER REMOVE THIS
                k = 10
                self.x += int(round(k*sin(self.angle)))
                self.y -= int(round(k*cos(self.angle)))
                self.boundary()

                my_ball.x += int(round(k*sin(my_ball.angle)))
                my_ball.y -= int(round(k*cos(my_ball.angle)))
                my_ball.boundary()
                # I am saving this dist_correction_angle as object parameter.
                # This has been initialized in the __init__ of Balls class
                self.correction_angle = abs(dist_correction_angle*180/pi) % 360

                sine_correction = sin(abs(dist_correction_angle))
                cosine_correction = cos(abs(dist_correction_angle))

                new_self_dist = int(self.dist * sine_correction)
                new_my_ball_dist = int(self.dist * cosine_correction)

                self.dist = new_self_dist
                my_ball.dist = new_my_ball_dist

                new_self_speed = self.speed * sine_correction
                new_my_ball_speed = self.speed * cosine_correction

                self.speed = new_self_speed
                my_ball.speed = new_my_ball_speed

                if (self.dist > 0) & (self.speed > 0):
                    self.offset_speed = float(self.speed - self.default_speed) / self.dist

                if (my_ball.dist > 0) & (my_ball.speed > 0):
                    my_ball.offset_speed = float(my_ball.speed - my_ball.default_speed) / my_ball.dist

    def move(self, dist=None, angle=None, speed=None, smear=False):
        from all_functions import *

        if dist is not None:
            self.dist = dist
        if angle is not None:
            self.angle = angle
        if speed is not None:
            self.speed = speed

        if (self.speed > 0) & (self.dist > 0):
            if not smear:
                show_table()
            self.is_pocketed(self.pocket_size)
            if self.pocketed == 1:
                self.dist = 0
                self.speed = 0
                if SOUNDS:
                    inpocketsound.play()
                return
            self.boundary()
            # This is equivalent to one time movement
            x_change = int(round(sin(self.angle) * self.speed))
            y_change = int(round(cos(self.angle) * self.speed))

            self.x += x_change
            self.y -= y_change

            self.boundary()

            self.dist -= hypot(x_change, y_change)
            # Movement of these units only :D

    def is_clicked(self, a, b):
        if hypot(self.x-a, self.y-b) <= self.size:
            return 1  # If the point (a,b) is inside the ball then return 1
        else:
            return 0  # Else return 0

    def is_pocketed(self, pocket_size):
        x_limits = (0, dispWidth/2, dispWidth)
        y_limits = (0, dispHeight)

        for i in x_limits:
            for j in y_limits:
                ball_dist = hypot(self.x - i, self.y - j)
                if ball_dist < pocket_size:
                    self.pocketed = 1
                    self.dist = 0  # So that the ball will not move any further
                    return 1
        return 0

    def give_me_pocket_angles(self, white_ball):
        # For a ball obj, this function returns a list containing movement
        # angles for all pockets

        from all_functions import *  # Required due usage of function get_angle

        a = [0, dispWidth/2, dispWidth]
        b = [0, dispHeight]
        rd.shuffle(a)
        rd.shuffle(b)

        t = []  # Empty list for angles towards pockets
        for i in a:
            for j in b:
                if self.am_I_near_to_pockets((i, j), white_ball):
                    t.append(get_angle((i, j), self))
        return t

    def am_I_near_to_pockets(self, pk_loc, white_ball):
        m, n = pk_loc
        p, q = white_ball.x, white_ball.y

        if hypot(p-m, q-n) > hypot(hypot(p-self.x, q-self.y), hypot(self.x - m, self.y - n)):
            return 1
        else:
            return 0


if __name__ == "__main__":
    print "This is running individually: Balls_class"
else:
    print "This is running inside someone: Balls_class"
