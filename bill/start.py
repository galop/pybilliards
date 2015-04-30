"""A billiards game in pygame.

.. moduleauthor:: Hardik, Rohan

"""

import pygame
from math import *
from pygame.locals import *
from modules.env_variables import *
from modules.all_functions import *
import adv_comp_mode as acm


pygame.mixer.pre_init(44100, -16, 2, 2048)  # setup mixer to avoid sound lag
pygame.init()  # initialize pygame
font = pygame.font.SysFont("ubuntu", 26)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
pygame.display.update()

try:
    pygame.mixer.music.load("assets/arab.mp3")
    pocketed = pygame.mixer.Sound("assets/pocketed.ogg")  # load sound
    splash_pic = pygame.image.load("assets/splash1.png").convert()
except:
    raise(UserWarning, "Could not load files in assets folder.")


class SOUND(object):
    """ Sound related settings.
    Used to turn sounds on or off during game play.

    """
    def __init__(self):
        """ Initialize SOUNDS instance

        SOUNDS = True implies sound is on.
        SOUNDS = False implies sound is off.
        """
        self.SOUNDS = True

    def toggle(self):
        """ Toggle sound settings
        """
        self.SOUNDS = False if self.SOUNDS else True


class Game(object):
    """Main Game class

        Implements methods to produce menus and graphical
        selection mechanism to choose gameplay modes from
        1. Single player mode (V/s. computer)
        2. Two player mode

    """
    def __init__(self):
        """
        Initial parameters

        gamemode = 1 - single player vs computer mode
        gamemode = 2 - two player mode
        """
        self.gamemode = 1
        self.decision = False
        self.b1 = Button("Single Player", (400, 400), True)
        self.b2 = Button("Two Player", (400, 450), False)

    def run(self):
        """ Starts the game.

        Starts game by showing splash screen and asking user the gameplay mode.
        """
        self.show_splash()
        self.askmode()
        if self.gamemode == 1:
            gameScore = acm.gameLoop("single")
        else:
            gameScore = acm.gameLoop("double")

    def show_splash(self):
        """ Show welcome screen

        Shows welcome screen with game name while arabian night is jamming in the background.
        Duration is fixed at 1 second.
        """
        # splash_pic = pygame.image.load("assets/splash1.png").convert()
        oldt = pygame.time.get_ticks()
        if SOUNDS:
            pygame.mixer.music.play()
        while(pygame.time.get_ticks() - oldt <= 1000):
            screen.blit(splash_pic, (0, 0))
            clock.tick(FPS)
            pygame.display.update()

    def askmode(self):
        """ Game mode selector

        Shows two options visually to select mode.
        A white disc is shown against currently active selection.

        .. note::
            Press Q to quit now.
        """
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
                    pygame.mixer.music.stop()
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
    """Button class for selecting gameplay mode

    Puts visual display of gameplay mode text.
    """
    def __init__(self, text, pos, choice=False):
        """ Button object.

        Args:
            text (str): Text to be displayed on Button
            pos (tuple): Position of button on screen
            choice (bool): If currently selected amongst many.
        """
        self.text = text
        self.pos = pos
        self.chose = choice
        self.opt = font.render(self.text, True, WHITE)

    def setON(self):
        """ Select this button.
        """
        self.chose = True

    def setOFF(self):
        """ Do not select this button.
        """
        self.chose = False

    def toggle(self):
        """ Toggle slection status
        """
        self.chose = False if self.chose else True

    def show(self):
        """ Draw button on display
        """
        X, Y = self.opt.get_size()
        screen.blit(self.opt, (self.pos[0] - 50, self.pos[1]))
        if self.chose:
            pygame.draw.circle(screen, WHITE, (self.pos[0]-80, self.pos[1]+15), 10)

if __name__ == "__main__":
    myGame = Game()
    myGame.run()
