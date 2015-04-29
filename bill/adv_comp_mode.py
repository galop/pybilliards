# This is implementation of COMP mode.
# Computer will play and pocket the balls available on screen
# --------------------------------------------------------------------------
import pygame
import random
from math import *

from classes_and_modules.all_functions import *
from classes_and_modules.env_variables import *
from classes_and_modules.Balls_class import Balls
from operator import *
from pygame.locals import *

pygame.init()
pygame.display.update()
Balls.shadow_img = pygame.image.load("assets/2.png").convert_alpha()
Balls.shading_img = pygame.image.load("assets/1.png").convert_alpha()


def gameLoop():

    gameExit = False
    gameOver = False
    all_balls = []  # List of balls
    cue_speed = default_speed  # Initial cue distance
    started = 0
    game_score = {1: {"Shots": 0, "Pocketed": 0},
                  2: {"Shots": 0, "Pocketed": 0},
                  3: {"Shots": 0, "Pocketed": 0}
                  }

    a, b = dispSize
    white_ball = Balls((a/4, b/2), size=my_ball_size, thickness=0, color=WHITE, speed=default_speed)
    # Other balls initialization
    for i in xrange(1, no_of_balls+1):
        all_balls.append(Balls(ball_loc[i], size=my_ball_size, color=ball_num_col_dict[i], number=i))

    while not gameExit:
        show_table()
        mouse_current_pos = pygame.mouse.get_pos()
        lineStart = (white_ball.x, white_ball.y)
        offset = tuple(map(sub, mouse_current_pos, lineStart))
        offset = Normalise_this(offset)
        kk = tuple([a * dispWidth for a in offset])
        lineEnd = tuple(map(add, lineStart, kk))
        pk = tuple([a*10 for a in offset])
        mm = tuple(map(add, lineStart, pk))
        lineStart = mm

        pygame.draw.aaline(gameDisplay, WHITE, lineStart, lineEnd)
        temp_all_balls = [my_ball for my_ball in all_balls if my_ball.pocketed == 0]
        all_balls = temp_all_balls
        if all_balls == []:
            gameOver = 1

        list_of_balls_with_white = all_balls + [white_ball]
        show_my_balls(list_of_balls_with_white)
        pygame.display.update()

        for moving_ball in list_of_balls_with_white:
            moving_ball.collision(list_of_balls_with_white)
            moving_ball.boundary()
            if (moving_ball.speed > 0) & (moving_ball.dist > 0):
                moving_ball.collision(list_of_balls_with_white)
                moving_ball.boundary()
            else:
                moving_ball.angle = 0
                moving_ball.dist = 0
                moving_ball.speed = 0

        if white_ball.pocketed == 1:
            a, b = dispSize
            white_ball = Balls((a/4, b/2), size=my_ball_size, thickness=0, color=WHITE)

        while gameOver:
            gameDisplay.fill(GREEN)
            msg2screen("Game over, press Q to quit or C to continue")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        game_score = {1: {"Shots": 0, "Pocketed": 0},
                                      2: {"Shots": 0, "Pocketed": 0},
                                      3: {"Shots": 0, "Pocketed": 0}
                                      }
                        gameLoop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameOver = True

        mouse_butt = pygame.mouse.get_pressed()
        # Comp Mode
        if mouse_butt[1] == 1:
            user_id = 3
            game_status_before = [temp_ball.pocketed for temp_ball in all_balls]
            no_of_pocketed_balls_before = sum(game_status_before)

            print "Advanced COMP MODE"
            # Pressed by the user manually, to start COMP to hit the right shot
            # Next shot placement, which ball to hit, is decided by the COMP,
            # depending on the some other factors (or may be randomly)

            show_pockets(my_pocket_size)
            pygame.display.update()

            # Following loop will extract hittable balls from all_balls 
            # Then we will decide which one to hit from those 
            for my_ball in all_balls:
                # List of other ball except current ball
                list_of_other_balls = all_balls[:]
                list_of_other_balls.remove(my_ball)
                balls_to_be_tested = []

                for other_ball in list_of_other_balls:
                    dist_white_other = hypot(white_ball.x-other_ball.x, white_ball.y-other_ball.y)
                    dist_my_other = hypot(my_ball.x-other_ball.x, my_ball.y-other_ball.y)
                    # Distance between white and other ball, and my_ball and other ball

                    dist_my_white = hypot(white_ball.x - my_ball.x, white_ball.y - my_ball.y)
                    if (dist_my_white > dist_white_other) & (dist_my_white > dist_my_other):
                        # then test this other_ball location, since it is in between my_ball and white_ball 
                        balls_to_be_tested.append(other_ball)
                if len(balls_to_be_tested) == 0:
                    my_ball.ok_to_hit = 1
                else:
                    x1, y1 = white_ball.x, white_ball.y
                    x2, y2 = my_ball.x, my_ball.y

                    # Testing for balls and their distance
                    for test_ball in balls_to_be_tested:
                        x3, y3 = test_ball.x, test_ball.y

                        # I will find of the perpendicular distance of point
                        # (x3, y3) from the line formed by the two points
                        # (x2, y2), and (x1, y1)

                        # Line equation in the form of Ax+ By+ C = 0
                        A = tan(atan2(y2-y1, x2-x1))  # slope of line
                        B = -1
                        C = y1 - A*x1
                        # Above formula is permutation from two point 
                        # line equation
                        # Perpendicular distance is given by
                        # Reference: goo.gl/mUFJSh
                        perp_dist = abs(A*x3 + B*y3 + C) / hypot(A, B)

                        seperation_factor = 1.5
                        if perp_dist > seperation_factor*(test_ball.size + white_ball.size):
                            # Here the multiplier 2 is taken, to be sure of distance 
                            my_ball.in_line_with_white_ball = 1
                        else:
                            my_ball.in_line_with_white_ball = 0
                            # Why to break? Beacause this means that some comes in between line of sight, hence can't test, break it 
                            break

                    if my_ball.in_line_with_white_ball == 1:    # If that ball is hittable after testing will all balls 
                        my_ball.ok_to_hit = 1
                    else:
                        my_ball.ok_to_hit = 0

            balls_ok_to_hit = [a_ball for a_ball in all_balls if a_ball.ok_to_hit == 1]

            # Advanced mode:
            if (len(balls_ok_to_hit) > 0) & ADV_MODE:

                a_ball = find_nearest_ball(balls_ok_to_hit, white_ball)
                a_ball.pk_list = a_ball.give_me_pocket_angles(white_ball)

                adv_mode_used = 1
                pk_loc_and_dist_from_white_dict = {}

                all_pk_loc = give_me_pocket_locations()
                for item in all_pk_loc:
                    mouse_current_pos = (a_ball.x, a_ball.y)
                    lineStart = item
                    offset = tuple(map(sub, mouse_current_pos, lineStart))
                    offset = Normalise_this(offset)

                    factor = 2*a_ball.size + hypot(lineStart[0] - mouse_current_pos[0], lineStart[1] - mouse_current_pos[1])
                    kk = tuple([a*factor for a in offset])
                    lineEnd = tuple(map(add, lineStart, kk))
                    pk = tuple([a*10 for a in offset])

                    mm = tuple(map(add, lineStart, pk))
                    lineStart = mm

                    lineEnd = tuple([int(a) for a in list(lineEnd)])
                    lineStart = tuple([int(a) for a in list(lineStart)])

                    pygame.draw.line(gameDisplay, RED, lineStart, lineEnd, 4)

                    pk_loc_and_dist_from_white_dict[lineEnd] = hypot(lineEnd[0] - white_ball.x, lineEnd[1] - white_ball.y)
                pygame.display.update()

                tt = min(pk_loc_and_dist_from_white_dict.items(), key=lambda x: x[1])
                x, y = tt[0]
                # (x, y) is point at which white ball should be hitted then
                # the ball will be pocketed
                ball_to_pocket_dist = tt[1]
                # This is the distance between the ball and its nearest pocket

                white_ball.angle = get_angle((x,y), white_ball)
                white_ball.speed = 8

                white_ball.dist = 2*(ball_to_pocket_dist + hypot(a_ball.x - white_ball.x, a_ball.y - white_ball.y))
                move_my_all_balls(list_of_balls_with_white)

                game_status_after = [temp_ball.pocketed for temp_ball in all_balls]
                no_of_pocketed_balls_after = sum(game_status_after)

                game_score[user_id]["Shots"] += 1
                game_score[user_id]["Pocketed"] += (no_of_pocketed_balls_after - no_of_pocketed_balls_before)

            else:
                print "Sorry can't use Advanced mode"
                adv_mode_used = 0
            # #===============================
            # Below is random hitting
            # To enable or disable below if condition "adv_mode_used"
            if (adv_mode_used == 0) or (RAND_MODE == 1):
                show_pockets(my_pocket_size)
                pygame.display.update()

                # This means that, there is atleast one ball which can be hit, but cannot be pocketed,
                # then, out of those balls_ok_to_hit, choose any one randomly and hit it 
                print "Choosing ball randomly to hit"
                temp_loc = random.randint(0, len(all_balls)-1)
                rand_ball_to_hit = all_balls[temp_loc]

                temp_angle = get_angle(white_ball_loc, rand_ball_to_hit)   # Passing the end point and Ball object to get the movement angle
                move_angle = temp_angle + pi

                # Here I am giving dist between 50 and 150, it is high distance . Its required so that ball can be hit hard 
                # rand_dist = random.randint(50,150)
                rand_dist = 100

                white_ball.dist = rand_dist
                white_ball.speed = 10
                white_ball.angle = move_angle

                move_my_all_balls(list_of_balls_with_white)
        else:
            for a_ball in list_of_balls_with_white:
                a_ball.angle = 0
                a_ball.dist = 0
        # User modes
        if (mouse_butt[2] == 1) or (mouse_butt[0] == 1):
            if (mouse_butt[2] == 1) and (mouse_butt[0] == 1):
                print "Please press one button at once"
                break
            elif (mouse_butt[2] != 1) & (mouse_butt[0] == 1):
                user_id = 1
            elif (mouse_butt[2] == 1) or (mouse_butt[0] != 1):
                user_id = 2

            game_status_before = [temp_ball.pocketed for temp_ball in all_balls]
            no_of_pocketed_balls_before = sum(game_status_before)
            print "======================================"
            print "User Mode:: User Acive: %d" % user_id
            print "======================================"
            started = 1
            # If pressed it acts as pulling the cue
            if cue_speed < cue_limit:
                cue_speed += 0.25  # If pressed I am increasing it
            else:
                pass
        else:
            if (cue_speed != white_ball.default_speed) & started:
                white_ball.speed = cue_speed

                mouse_current_pos = pygame.mouse.get_pos()
                a, b = white_ball.x, white_ball.y
                c, d = mouse_current_pos

                white_ball.dist = 2*(hypot(a-c, b-d))
                # I will hit the white ball with cue
                # Get mouse location, to hit
                mouse_current_pos = pygame.mouse.get_pos()
                white_ball.angle = get_angle(mouse_current_pos, white_ball)

                move_my_all_balls(list_of_balls_with_white)
                # and then I will assign the distance back to default_speed
                cue_speed = white_ball.default_speed

                game_status_after = [temp_ball.pocketed for temp_ball in all_balls]
                no_of_pocketed_balls_after = sum(game_status_after)

                game_score[user_id]["Shots"] += 1
                game_score[user_id]["Pocketed"] += (no_of_pocketed_balls_after - no_of_pocketed_balls_before)

        clock.tick(FPS)

    # pygame.quit()
    # quit()

if __name__ == '__main__':
    gameLoop()
