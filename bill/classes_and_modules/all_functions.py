
from classes_and_modules.env_variables import *
# from classes_and_modules.Balls_class import Balls


def msg2screen(msg, x_loc=dispWidth/2, y_loc=dispHeight/2, color=BLACK):
    """ This function will print string msg to screen at
        respective location
    """
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [x_loc,  y_loc])


def show_pockets(pocket_size):
    """ This function displays pockets at six (standard) locations. 
        Size of pocket is taken from user.
    """
    a = (0, dispWidth/2, dispWidth)
    b = (0, dispHeight)

    for i in a:
        for j in b:
            pygame.draw.circle(gameDisplay, BLACK, (i, j), pocket_size, 0)


def get_angle(point_loc, Ball_obj):
    """ This function gives movement angle for Ball_obj (w.r.t to Vertical y-axis)
        to move towards point defined point_loc tuple.
    """
    a, b = point_loc
    c, d = Ball_obj.x, Ball_obj.y
    t1 = (a - c)
    t2 = (-1)*(b - d)

    move_angle = atan2(t1, t2)

    return move_angle %(2*pi)


def move_my_all_balls(list_of_balls):
    """ This function moves Ball objects contained in list_of_balls. 
        The whiile loop runs till all Ball objects in list_of_balls has either speed = 0, or dist = 0.
        It works as all movable Ball objects are moved by one unit distance and, their positions
        are also modified, considering the collision or boundary of table.
    """
    speed_sum_vect = [a_ball.speed for a_ball in list_of_balls]
    speed_sum = sum(speed_sum_vect)

    dist_sum_vect = [a_ball.dist for a_ball in list_of_balls]
    dist_sum = sum(dist_sum_vect)

    for a_ball in list_of_balls:
        if (a_ball.dist > 0) & (a_ball.speed > 0):
            a_ball.offset_speed = float(a_ball.speed - a_ball.default_speed) / a_ball.dist

    fric = 1.05
    while (speed_sum > 0) & (dist_sum > 0):
        for a_ball in list_of_balls:
            a_ball.offset_speed = fric * a_ball.offset_speed
            a_ball.disp()

        pygame.display.update()

        for moving_ball in list_of_balls:
            if (moving_ball.speed > 0) & (moving_ball.dist > 0):
                reduced_speed = moving_ball.speed - moving_ball.offset_speed
                moving_ball.move(speed = reduced_speed)
                moving_ball.boundary()
            else:
                moving_ball.angle = 0
                moving_ball.dist = 0
                moving_ball.speed = 0

        for moving_ball in list_of_balls:
            if (moving_ball.speed > 0) & (moving_ball.dist > 0):
                moving_ball.collision(list_of_balls)
                moving_ball.boundary()
            else:
                moving_ball.angle = 0
                moving_ball.dist = 0
                moving_ball.speed = 0

        dist_sum_vect = [a_ball.dist for a_ball in list_of_balls]
        dist_sum = sum(dist_sum_vect)
        speed_sum_vect = [a_ball.speed for a_ball in list_of_balls]
        speed_sum = sum(speed_sum_vect)


def is_it_in_my_list(elem_to_search, in_list, pass_range):
    """ This function return 1 if elem_to_search is present in in_list,
        within pass_range provided by user.
    """
    # This function will return 1, if elem_to_search is present in pass_range of in_list
    # i.e. pass_range = 20 => 20% difference is ok,

    for item in in_list:
        if (abs(item - elem_to_search)/item >= pass_range):
            return 1
        else:
            return 0


def Normalise_this(in_tup):
    """ This function normalises the 2 point in_tup, by dividing each element by
        its magnitude.
    """
    a, b = in_tup
    t = hypot(a, b)
    if t != 0:
        return [float(a)/t, float(b)/t]
    else:
        return [0, 0]


def show_my_balls(list_of_balls):
    """ This function invokes disp method for Ball objects present in list_of_balls.
    """
    for a_ball in list_of_balls:
        a_ball.disp()


def show_table():
    """ This function loads simple table enviroment graphics. Fills screen with GREEN and 
        then draws pockets over it using show_pockets() function.
    """
    gameDisplay.fill(GREEN)
    show_pockets(my_pocket_size)
    # pygame.display.update()


def give_me_pocket_locations():
    """ This function return list containing pockets location, dynamically depending on
        size of table.
    """
    a = (0, dispWidth/2, dispWidth)
    b = (0, dispHeight)
    t = []

    for i in a:
        for j in b:
            t.append((i,j))
    return t


def find_nearest_ball(list_of_balls, white_ball):
    """ This function returns a Ball object from input list_of_balls, which is nearest to
        the Cue ball i.e. white_ball.
    """
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