import unittest
import baaalls_6 as game

class TestMyGame(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_rand_Ball(self):
        # self.assertEqual(type(create_rand_Ball(20)), game.Balls)
        x = game.create_rand_Ball(20)
        self.assertEqual(x.size, 20)

    def test_balls_is_pocketed(self):
        x = game.Balls((0,0), 20)
        y = game.Balls((30,30), 10)
        self.assertEqual(x.pocketed, 1)
        self.assertEqual(y.pocketed, 0)

    def test_get_slope(self):
        self.assertEqual(round(game.get_slope(0,0,20,20)), 1)
        self.assertEqual(round(game.get_slope(0,0,0,0)), 0)

    def test_ball_got_hit(self):
        x = game.Balls((45,45), 20)
        point = (42,42)
        self.assertEqual(game.ball_got_hit(point, x), 1)

    def test_in_boundary(self):
        testpt = (-34, 100)
        self.assertEqual(game.in_boundary(testpt), False)

    
 



    # def test_offset(self):
    #     self.assertEqual(min(b.offset(x,20,20)), 0)
    #     self.assertLessEqual(max(b.offset(x,20,20)), 20)

    # def test_transform(self):
    #     self.assertEqual(type(b.transform(x, y, 20, 20)), tuple)
    #     self.assertEqual(type(b.transform(x, y, 20, 20)[0]), list)
    #     self.assertEqual(type(b.transform(x, y, 20, 20)[1]), list)
    #     self.assertEqual(type(b.transform(x, y, 20, 20)[0][0]), int)
    #     self.assertEqual(type(b.transform(x, y, 20, 20)[1][0]), int)
    #     self.assertEqual(type(b.transform(x, y, 20, 20)[0][-1]), int)
    #     self.assertEqual(len(b.transform(x, y, 20, 20)[1]), 20)


if __name__ == "__main__":
    unittest.main()