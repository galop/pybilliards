import unittest
from comp_mode import *
import comp_mode as game

def rad2deg(rad_angle):
    import math
    return (rad_angle*180/math.pi)

class TestMyGame(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_balls_collision_fixed_loc(self):
        # self.assertEqual(type(create_rand_Ball(20)), game.Balls)
        # x = game.create_rand_Ball(20)
        x, y        = dispWidth/2, dispHeight/2
        print x, y

        # first_ball  = Balls((x, y))
        # first_ball.dist = 100
        # first_ball.angle = 2*pi + pi/4
        # # print "First_angle:" + str(rad2deg(first_ball.angle))
        # move_my_all_balls([first_ball])
        # first_ball.disp()

        #========================================================================
        arr1 = [1, -1]
        arr2 = [-1, 1]
        
        temp_angle = 3*pi/2 - pi/4
        
        for i in arr1:
            if i == -1:
                arr2 = [1, -1]

            for j in arr2:
                print i, j

                first_ball  = Balls((x, y))
                first_ball.disp()

                x1, y1      = x+i*100, y+j*100
                white_ball  = Balls((x1, y1),color = (255, 255, 255))
                white_ball.disp()
                # Now I will strike the two balls and see where they go
                
                white_ball.angle = temp_angle
                temp_angle += pi/2
                white_ball.dist     = 300

                the_two_balls = [first_ball, white_ball]

                print "White_angle:" + str(rad2deg(white_ball.angle) % 360), "First_angle:" + str(rad2deg(first_ball.angle) % 360)
                move_my_all_balls(the_two_balls)
                # white_ball.move_with_collision_correction_2(dist = 300, list_of_ball_objects = the_two_balls, smear = False)

                print "White_angle:" + str(rad2deg(white_ball.angle) % 360), "First_angle:" + str(rad2deg(first_ball.angle) % 360)
        #========================================================================
        pass
        
    def test_balls_collision_rand_loc(self):
        # self.assertEqual(type(create_rand_Ball(20)), game.Balls)
        # x = game.create_rand_Ball(20)
        x, y        = dispWidth/2, dispHeight/2
        print x, y

        # first_ball  = Balls((x, y))
        # first_ball.dist = 100
        # first_ball.angle = 2*pi + pi/4
        # # print "First_angle:" + str(rad2deg(first_ball.angle))
        # move_my_all_balls([first_ball])
        # first_ball.disp()

        #========================================================================
        
        
        
        temp_angle = 3*pi/2 - pi/4
        
        for i in xrange(2):
            for j in xrange(2):
                print i, j

                first_ball  = Balls((x, y))
                first_ball.disp()

                x1 = random.randint(x-100, x+100)
                y1 = random.randint(y-100, y+100)
                
                white_ball  = Balls((x1, y1),color = (255, 255, 255))
                white_ball.disp()
                # Now I will strike the two balls and see where they go
                
                white_ball.angle = get_angle((first_ball.x, first_ball.y), white_ball)
                
                white_ball.dist     = 600

                the_two_balls = [first_ball, white_ball]

                print "White_angle:" + str(rad2deg(white_ball.angle) % 360), "First_angle:" + str(rad2deg(first_ball.angle) % 360)
                move_my_all_balls(the_two_balls)
                # white_ball.move_with_collision_correction_2(dist = 300, list_of_ball_objects = the_two_balls, smear = False)

                print "White_angle:" + str(rad2deg(white_ball.angle) % 360), "First_angle:" + str(rad2deg(first_ball.angle) % 360)
        #========================================================================
        pass


    
 

if __name__ == "__main__":
    unittest.main()