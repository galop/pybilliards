
from classes_and_modules.env_variables import *
from classes_and_modules.Balls_class import Balls


def create_rand_Ball(size):
    x = random.randint(size, dispWidth-size)
    y = random.randint(size, dispHeight-size)
    return Balls((x, y), size)


def msg2screen(msg, x_loc=dispWidth/2, y_loc=dispHeight/2, color=BLACK):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [x_loc,  y_loc])


def show_pockets(pocket_size):
    a = (0, dispWidth/2, dispWidth)
    b = (0, dispHeight)

    for i in a:
        for j in b:
            pygame.draw.circle(gameDisplay, BLACK, (i, j), pocket_size, 0)
            # pygame.display.update()


def stick(block_size, stickList):  # This will print our stick of finite length
    for each in stickList:
        pygame.draw.rect(gameDisplay, blue, [each[0], each[1], block_size, block_size])


def get_points(x1, y1, x2, y2, curr_dist, m, choice):
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
    # a = dispWidth/4
    # b = 3*dispHeight/4

    if abs(y2-y1) >= abs(x2-x1):
        if (y2 >= y1) ^ choice:
        # y2 = y2-1
            y = y1 - curr_dist
        else:
        # y2 = y2+1
            y = y1 + curr_dist

        x = x2 + round(m*(y - y2))  # From (x2,y2) and y selected, x will be found out :D
        # s = "<<--------Inside y------->>  " + str(m)
    else:
        if (x2 >= x1) ^ choice:
            x = x1 - curr_dist
        else:
            x = x1 + curr_dist

        y = y2 + round(m*(x - x2))  # From (x2,y2) and y selected, x will be found out :D
        # s = "<<--------Inside x------->>  " + str(m)

    # msg2screen(s,a,b)
    return (x, y)

def new_get_slope(x1, y1, x2, y2):
    # p = dispWidth/4
    # q = 3*dispHeight/4
    # s = "x1, y1, x2, y2: " + str(x1) + ":" + str(x1) + ":" + str(y1) + ":" + str(x2) + ":" + str(y2)

    if (y2-y1) != 0:
        m = float(x2-x1)/(y2-y1)
    else:
        m = abs(x2-x1)*10**2 # I am returning a high value, equivalent to infinity.
        if x2 > x1:
            m = m * -1
    return m

def get_slope(x1, y1, x2, y2):
    # p = dispWidth/4
    # q = 3*dispHeight/4
    # s = "x1, y1, x2, y2: " + str(x1) + ":" + str(x1) + ":" + str(y1) + ":" + str(x2) + ":" + str(y2)
    # # if (x2-x1)!=0:
    #                                 #          (y2-y1)
    #                 #                (y-y1) =  ------- * (x-x1)                                      
    #                            #               (x2-x1) 
    #     m1 = float(y2-y1)/(x2-x1)
    #     m = m1
    #     s = "you are is m111111111"
    #     # return m1

    # elif (y2-y1)!=0:
    #                                 #          (x2-x1)
    #                 #                (x-x1) =  ------- * (y-y1)                                      
    #                            #               (y2-y1)                     
    #     m2 = float(x2-x1)/(y2-y1)
    #     m = m2
    #     s = "you are is m222222222"
    #     # return m2
    # # msg2screen(s,p,q)
    y_diff = (y2-y1)
    x_diff = (x2-x1)

    m = tan(atan2(y_diff, x_diff))
    return m


def get_angle(point_loc, Ball_obj):
    # temp1 = point_loc[0] - Ball_obj.x
    # temp2 = -1*(point_loc[1] - Ball_obj.y)  # This -ve sign is to incorporate the inverted y-axis :D

    a, b = point_loc
    c, d = Ball_obj.x, Ball_obj.y
    t1 = (a - c)
    t2 = (-1)*(b - d)

    # if temp2 == 0:
    #     move_angle = (pi/2) * (temp1/abs(temp1)) # This is for the sign of than angle also :D
    # else:
    #     move_angle = atan(float(temp1)/temp2)

    move_angle = atan2(t1, t2)

    return move_angle %(2*pi)

def ball_got_hit(start_point, Ball_obj):
    hamming_dist = sqrt((start_point[0]- Ball_obj.x)**2 + (start_point[1]- Ball_obj.y)**2)

    if hamming_dist < Ball_obj.size:
        return 1
    else:
        return 0


def trace_the_shot(start_point, end_point, m, mouse_pos):
    # This only projects a line from the stick with some finite distnace :D
    # Ball touch is not included here :D

    move_dist = sqrt((end_point[0] - mouse_pos[0])**2 + (end_point[1] - mouse_pos[1])**2)
    # get_points(x1,y1,x2,y2,curr_dist,m,choice):
    a,b = start_point[0], start_point[1], 
    c,d = end_point[0], end_point[1]

    # m = get_slope(a,b,c,d)
    trace_point = get_points(a, b, c, d, move_dist, m, 0)  # Here choice = 0, Since I want to find the trace point :D

    point_to_draw = []
    point_to_draw.append(start_point)       # Line will start from here
    # Now I am checking for any boundary reflection of that trace line :D

    temp_dist = 1
    # points_on_line = []

    while temp_dist <= move_dist:
        # m = get_slope(a,b,c,d)
        # if abs(m)>1:
        #     m = 1/m

        temp_point = get_points(a, b, c, d, temp_dist, m, 0)  # Here choice = 0, Since I want to find the trace point :D
        temp_dist += 1
        # points_on_line.append(temp_point)

        x,y = temp_point
        # if x < 0 or y < 0 or x > (dispWidth ) or y > (dispHeight ):  
        # # Here the condition is written in special way, so that point to added has positive cooradinates :D
        #     last_point = points_on_line[-2]   
        #     # I want to add the second last point which was added
        #     # The last point which was added is the out of boundary point :D
        #     point_to_draw.append(last_point)

        #     # Modifying the "get_points" function call, so that line will be traced even after the boundary was crossed :D

        #     # Checking which boundary was crossed
        #     # 
        #     #                                 this is boundary no. 1   (x---->--->)
        #     #                               --------------------------
        #     #                               |                        |
        #     #                               |                        |
        #     #     this is boundary no. 4    |                        |  this is boundary no. 2
        #     #                               |                        |
        #     #                               |                        |
        #     #                               --------------------------
        #     #                                   this is boundary no. 3

        #     if x < 0 or x > (dispWidth ):
        #         x = dispWidth - (x % dispWidth)

        #     if y < 0 or y > (dispHeight ):
        #         y = dispHeight - (y % dispHeight)

        #     # Now after solving boundary problem, we need to modify the start and end points so that the line is traced correct
        #     # Hence, "new end point" is the boundary point that added
        #     # and "new start point" will be the out of boundary point which has been corrected as above :D
        #     c,d = last_point        # new end point
        #     a,b = x,y               # new start point :D
    
        k = 0 
        # This is special unit :D

        if x < k or y < k or x > (dispWidth -k) or y > (dispHeight -k):  
            
            # Here the condition is written in special way, so that point to added has positive cooradinates :D
            
            # Modifying the "get_points" function call, so that line will be traced even after the boundary was crossed :D

            # Checking which boundary was crossed
            # 
            #                                 this is boundary no. 1   (x---->--->)
            #                               --------------------------
            #                               |                        |
            #                               |                        |
            #     this is boundary no. 4    |                        |  this is boundary no. 2
            #                               |                        |
            #                               |                        |
            #                               --------------------------
            #                                   this is boundary no. 3
            
            

            if x < k or x > (dispWidth - k):
                x = dispWidth - (x % dispWidth)
                if x < k:
                    x_cordi = 0

                    c = c
                    d = -d 
                    
                else:
                    x_cordi = dispWidth

                    c = c
                    d = 2*dispHeight - d

                y_cordi = m*x_cordi + (b - m*a)  

            if y < k or y > (dispHeight -k):
                y = dispHeight - (y % dispHeight)
                if y < k:
                    y_cordi = 0

                    c = -c
                    d = d 

                else:
                    y_cordi = dispHeight

                    c = 2*dispWidth - c
                    d = d

                x_cordi = (1/m)*y_cordi + (a - (1/m)*b)  # You can replace y2 by y2 , and x2 by x1 also :D

            last_point = (x_cordi, y_cordi)
            point_to_draw.append(last_point)

            # Now after solving boundary problem, we need to modify the start and end points so that the line is traced correct
            # Hence, "new start point" is the boundary point that added
            # and "new end point" will be calculated as below (I have reflected previous end point to get this new one :D)
            a,b = last_point        # new start point
                                    # new start point :D already modified
         # After finishing the while loop, I must add the last point which got traced, to list of "point_to_draw"       

        m = tan(pi - atan(m))  # AFter coming out of the loop for correcting x,y change the slop of the line :D
        if abs(m)>1:
            m = 1/m


    point_to_draw.append(temp_point)

     # I will now draw lines in between the point in my list "point_to_draw"
     # i.e. line between 1st and 2nd, then between 2nd and 3rd, and so on
     # Why/when "point_to_draw" will have more than 2 points??
     # If there is reflection due to surface then only more than 2
     # If no reflection at all then only 2 point in the list "point_to_draw" :D
    print point_to_draw
    for i in xrange(len(point_to_draw) - 1):  
     # Ques: Why    len(point_to_draw) -1    ? 
     # Ans : Because to no pair for the last point :D
        # pygame.draw.aaline(gameDisplay, (0, 255, 0), point_to_draw[i], point_to_draw[i+1])
        # pygame.draw.line(gameDisplay, (255, 0, 0), point_to_draw[i], point_to_draw[i+1],20)
        pygame.display.update()
    aa,bb = trace_point
    # aa = aa % dispWidth
    # bb = bb % dispHeight
    new = aa,bb
    pygame.draw.line(gameDisplay, (255, 0, 0), point_to_draw[0], new,2)
    pygame.display.update()
    # p = dispWidth/4 - 100
    # q = 3*dispHeight/4 + 100
    # s = "tracing the shot.... No of lines to be drawn is : "+ str(len(point_to_draw) -1) +"::: " + str(point_to_draw)
    # msg2screen(s,p,q)
    # pygame.display.update()


def in_boundary(trace_point):
    a, b = trace_point
    if a < 0 or b < 0 or a > dispWidth or b > dispHeight:
        return 0
    else:
        return 1

# def get_boundary_point(trace_point, m): # This function will be called only if the point is out of boundary :D
#     a,b = trace_point


def get_elevation(start_point, end_point):
    a, b = start_point
    c, d = end_point
    new_m = new_get_slope(a, b, c, d)  # Calculating this slope :D

    if new_m > 0:   # First and Third quadrant
        if b < d:
            elevation = pi + atan(new_m)
        else:
            elevation = atan(new_m)
    else:           # Second and Fourth quadrant
        if b < d:
            elevation = pi + atan(new_m)
        else:
            elevation = 2*pi + atan(new_m)

    return elevation

def trace_for_rotated_white_ball_shot(my_ball, white_ball, list_of_ball_objects, move_dist=50):
    start1 = (white_ball.x, white_ball.y)
    start2 = (my_ball.x, my_ball.y)

    ball_point = Balls(start1, 3, color = (0,0,255), angle=white_ball.angle)
    big_ball_of_size_of_white = Balls(start1, white_ball.size, color=BLACK, angle=white_ball.angle)
    final_trace_ball_point = Balls(start2, 3, color = (255, 255, 0))

    list_1 = [such_ball for such_ball in list_of_ball_objects if such_ball != white_ball]
    list_2 = [such_ball for such_ball in list_of_ball_objects if such_ball != my_ball]

    trace_for_while_ball_shot(start2, start1, list_1, move_dist = 50, start_point = 1, trace_angle = ball_point.angle)

    ball_point.move_with_collision_correction_2_rotation(dist = 50, angle = ball_point.angle, list_of_ball_objects = list_1, speed = 8, smear = True , show_me = True, ball_will_got_hit = final_trace_ball_point)
    big_ball_of_size_of_white.move_with_collision_correction_2_rotation(dist = 50, angle = ball_point.angle, list_of_ball_objects = list_1, speed = 8, smear = True , show_me = False, ball_will_got_hit = final_trace_ball_point)
    # Value of angle of "final_trace_ball_point" is changed twice :D
    # Second one will be the final :D
    # Why to do this?
    # By first move_.. I am showing a small point tracing
    # By second move_.. I am moving a white_ball like object so as to get the right
    # movement angle for "final_trace_ball_point" :D


    # temp_value = trace_for_while_ball_shot(start2, start1, list_2, move_dist = final_trace_ball_point.dist, trace_angle = final_trace_ball_point.angle, start_point = 2)
    temp_value = trace_for_while_ball_shot(start2, start1, list_2, move_dist = 50, trace_angle = final_trace_ball_point.angle, start_point = 2)
    return temp_value


def trace_for_while_ball_shot(my_ball_loc, white_ball_loc, list_of_ball_objects, move_dist=50, trace_angle=None, start_point=2):
    slope_angle = get_elevation(my_ball_loc, white_ball_loc)

    if start_point == 2:
        ball_point = Balls(my_ball_loc, 3, color=(255,0,0))
    else:
        ball_point = Balls(white_ball_loc, 3, color=(0,255,0))

    # kkk = 2*pi/2
    kkk = pi
    
    if trace_angle == None:
        trace_angle = kkk - (slope_angle)

    # Note: The method is used is different :D
    # Its detection only :D no correction is intended since its only trace :D
    in_journey = ball_point.move_with_collision_detection(move_dist, trace_angle, list_of_ball_objects, speed=8, smear=True, show_me=False)                            
    # pygame.display.update()

    will_it_be_pocketed = in_journey            # yes for 1, and no for 0 :D

    return will_it_be_pocketed


def new_trace_the_shot(start_point, end_point, elevation, mouse_pos):
    a, b = end_point
    c, d = mouse_pos
    e, f = start_point
    move_dist = sqrt((a-c)**2 + (b-d)**2)

    # Balls(self,(x,y),size, thickness=0, color=(0,0,255)):
    ball_point = Balls(start_point, 3, color=RED)
    kkk = pi
    slope_angle = elevation
    trace_angle = kkk - (slope_angle)

    # Ball.move(self,dist, angle, speed)
    ball_point.move(move_dist, trace_angle, speed = 10, smear=True)

    # s = "tracing the shot...................(" + str(slope_angle*180/pi) +").........(" + str(trace_angle*180/pi) + ")"
    # print s


def move_my_all_balls(list_of_balls):
    speed_sum_vect = [a_ball.speed for a_ball in list_of_balls]
    speed_sum = sum(speed_sum_vect)

    dist_sum_vect = [a_ball.dist for a_ball in list_of_balls]
    dist_sum = sum(dist_sum_vect)

    for a_ball in list_of_balls:
        # a_ball.speed = 10
        if (a_ball.dist > 0) & (a_ball.speed > 0):
            a_ball.offset_speed = float(a_ball.speed - a_ball.default_speed) / a_ball.dist

    while (speed_sum > 0) & (dist_sum > 0):
        # print "dist_sum: " + str(dist_sum)
        # show_my_balls(list_of_balls)
        for a_ball in list_of_balls:
            a_ball.disp()
        pygame.display.update()

        for moving_ball in list_of_balls:
            if (moving_ball.speed > 0) & (moving_ball.dist > 0):
                # reduced_speed = moving_ball.speed - moving_ball.offset_speed
                moving_ball.collision_2(list_of_balls)
                moving_ball.boundary()
                # moving_ball.dist -= 1
            else:
                moving_ball.angle = 0
                moving_ball.dist = 0
                moving_ball.speed = 0

        for moving_ball in list_of_balls:
            if (moving_ball.speed > 0) & (moving_ball.dist > 0):
                reduced_speed = moving_ball.speed - moving_ball.offset_speed
                moving_ball.move_with_collision_correction_3(speed = reduced_speed, list_of_ball_objects = list_of_balls)
                moving_ball.boundary()
                # moving_ball.dist -= 1
            else:
                moving_ball.angle = 0
                moving_ball.dist = 0
                moving_ball.speed = 0

        for moving_ball in list_of_balls:
            if (moving_ball.speed > 0) & (moving_ball.dist > 0):
                # reduced_speed = moving_ball.speed - moving_ball.offset_speed
                moving_ball.collision_2(list_of_balls)
                moving_ball.boundary()
                # moving_ball.dist -= 1
            else:
                moving_ball.angle = 0
                moving_ball.dist = 0
                moving_ball.speed = 0

        dist_sum_vect = [a_ball.dist for a_ball in list_of_balls]
        dist_sum = sum(dist_sum_vect)
        speed_sum_vect = [a_ball.speed for a_ball in list_of_balls]
        speed_sum = sum(speed_sum_vect)

def is_it_in_my_list(elem_to_search, in_list, pass_range):
    # This function will return 1, if elem_to_search is present in pass_range of in_list
    # i.e. pass_range = 20 => 20% difference is ok,

    for item in in_list:
        if (abs(item - elem_to_search)/item >= pass_range):
            return 1
        else:
            return 0
def Normalise_this(in_tup):
    a, b = in_tup
    t = hypot(a, b)
    if t != 0:
        return [float(a)/t, float(b)/t]
    else:
        return [0, 0]

def show_my_balls(list_of_balls):
    for a_ball in list_of_balls:
        a_ball.disp()

def show_table():
    gameDisplay.fill(GREEN)
    show_pockets(my_pocket_size)
    # pygame.display.update()

def give_me_pocket_locations():
    a = (0, dispWidth/2, dispWidth)
    b = (0, dispHeight)
    
    t = []

    for i in a:
        for j in b:
            t.append((i,j))
    return t

def find_nearest_ball(list_of_balls, white_ball):
    if len(list_of_balls) == 1:
        return list_of_balls[0]

    dist_dict = {}
    for a_ball in list_of_balls:
        temp_dist = hypot(a_ball.x - white_ball.x, a_ball.y - white_ball.y)
        dist_dict[temp_dist] = a_ball
    tt = min(dist_dict.items(), key=lambda x: x[0])
    return tt[1]

if __name__ == "__main__":
    print "This is running individually: all_functions"
else:
    print "This is running inside someone :d : all_functions"