import pygame
from math import *
from pygame.locals import *
from classes_and_modules.env_variables import *
from classes_and_modules.all_functions import *
from classes_and_modules.Balls_class import Balls
import adv_comp_mode as acm

TITLE = "pyBilliards"
SOUNDS = True
# GAMEMODE = 1  # 1: sinle player, 2: Two player

pygame.mixer.pre_init(44100, -16, 2, 2048)  # setup mixer to avoid sound lag
pygame.init()  # initialize pygame
font = pygame.font.SysFont("ubuntu", 24)
font.set_bold(True)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
# scorecard = pygame.Surface((400, 80))
# scorecard.fill(SCORECARDCOLOR)
# settingpanel = pygame.Surface((400, 80))
# settingpanel.fill(SCORECARDCOLOR)
# powerbar = pygame.Surface((800, 20))
# powerbar.fill(BLACK)
pygame.display.update()

try:
    # pygame.mixer.music.load("assets/levels.ogg")  # load music
    pocketed = pygame.mixer.Sound("assets/pocketed.ogg")  # load sound
    hit = pygame.mixer.Sound("assets/wood2.ogg")  # load sound
    splash_pic = pygame.image.load("assets/splash1.png").convert()
    splash_chime = None
except:
    raise(UserWarning, "Could not load files in assets folder.")


# class GAMEMODE():
#     def __init__(self):
#         self.state = 1

#     def toggle(self):
#         if self.state == 1:
#             self.state = 2
#         else:
#             self.state = 1


class Gamer(object):
    """Main Game class

        Implements methods to produce menus and graphical
        selection mechanism to choose gameplay modes from
        1. Single player mode (V/s. computer)
        2. Two player mode

    """
    def __init__(self):
        self.gamemode = 1
        self.decision = False
        self.b1 = Button("Single Player", (400, 400), True)
        self.b2 = Button("Two Player", (400, 450), False)

    def run(self):
        self.show_splash()
        self.askmode()
        if self.gamemode == 1:
            acm.gameLoop()
        else:
            acm.gameLoop()

    def show_splash(self):
        # splash_pic = pygame.image.load("assets/splash1.png").convert()
        oldt = pygame.time.get_ticks()
        while(pygame.time.get_ticks() - oldt <= 1500):
            screen.blit(splash_pic, (0, 0))
            clock.tick(FPS)
            pygame.display.update()

    def askmode(self):
        self.b1.show()
        self.b2.show()
        while not self.decision:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            key = pygame.key.get_pressed()
            if key[K_ESCAPE] or key[K_q]:  # Finally key debounce works
                exit()
            if key[K_DOWN]:
                self.b1.setOFF()
                self.b2.setON()
                self.gamemode = 2
                if SOUNDS:
                    pocketed.play()
            if key[K_UP]:
                self.b1.setON()
                self.b2.setOFF()
                self.gamemode = 1
                if SOUNDS:
                    pocketed.play()
            if key[K_RETURN]:
                if SOUNDS:
                    pocketed.play()
                if self.b1.chose is True:
                    print("User selected mode is Single Player.")
                    self.decision = True
                    self.gamemode = 1
                else:
                    print("User selected mode is Two player.")
                    self.decision = True
                    self.gamemode = 2
            screen.blit(splash_pic, (0, 0))
            self.b1.show(), self.b2.show()
            pygame.display.update()
            clock.tick(FPS)


class Button(object):
    """Button class for selecting gameplay mode"""
    def __init__(self, text, pos, choice=False):
        self.text = text
        self.pos = pos
        self.chose = choice
        self.opt = font.render(self.text, True, WHITE)

    def setON(self):
        self.chose = True

    def setOFF(self):
        self.chose = False

    def toggle(self):
        self.chose = False if self.chose else True

    def show(self):
        X, Y = self.opt.get_size()
        screen.blit(self.opt, (self.pos[0] - 50, self.pos[1]))
        if self.chose:
            pygame.draw.circle(screen, WHITE, (self.pos[0]-70, self.pos[1]+10), 10)

# class Splash():
#     def __init__(self):
#         self.createTime = pygame.time.get_ticks()
#         self.splash_pic = pygame.image.load("assets/splash1.png").convert()

#     def show(self):
#         screen.blit(self.splash_pic, (0, 0))


myGame = Gamer()
# myGame.show_splash()
# myGame.askmode()
myGame.run()

# gameOver = False
# while not gameOver:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             gameOver = True

#     # show_mode()
#     # screen.fill(GREEN)
#     pygame.display.update()
#     clock.tick(FPS)
