#!/usr/bin/python

import pygame
# import time
import random
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
FPS = 20
dispHeight = 600
dispWidth = 800
font = pygame.font.SysFont(None, 25)

gameDisplay = pygame.display.set_mode((dispWidth, dispHeight))
pygame.display.set_caption('theVault')
clock = pygame.time.Clock()

pygame.display.update()


def msg2screen(msg, color=black):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [dispWidth/2,  dispHeight/2])


def snake(block_size, snakeList):
    for each in snakeList:
        pygame.draw.rect(gameDisplay, blue, [each[0], each[1], block_size, block_size])


def gameLoop():
    lead_x = dispWidth/2
    lead_y = dispHeight/2
    lead_x_del = 0
    lead_y_del = 0
    block_size = 10
    gameExit = False
    gameOver = False
    snakeLength = 1
    snakeList = []
    prev_key = 0        # This is initialisation before the using in program :D
    once = 0

    randAppleX = round(random.randrange(0, dispWidth - block_size)/10.0)*10
    randAppleY = round(random.randrange(0, dispHeight - block_size)/10.0)*10

    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    while not gameExit:
        print "General loop :D"
        while gameOver:
            gameDisplay.fill(white)
            msg2screen("Game over, press Q to quit or C to continue.")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:

                mods = pygame.key.get_mods()        # Assining a name, to use easily :D

                if event.key == pygame.K_LEFT:
                    print "This is K_LEFT"

                    if lead_x_del != block_size:
                        lead_x_del = -block_size
                        lead_y_del = 0
                    # lead_x_del = -block_size
                    # lead_y_del = 0
                    
                    if mods & pygame.KMOD_CTRL:
                        print "Left + CTRL pressed :D"
                        if (lead_x_del != block_size) or (lead_y_del != block_size):
                            lead_x_del = -block_size
                            lead_y_del = lead_x_del

                elif event.key == pygame.K_RIGHT:
                    print "This is K_RIGHT"
                    if lead_x_del != -block_size:
                        lead_x_del = block_size
                        lead_y_del = 0
                    
                    
                    if mods & pygame.KMOD_CTRL:
                        print "Right + CTRL pressed :D"
                        if (lead_x_del != -block_size) or (lead_y_del != -block_size):
                            lead_x_del = block_size
                            lead_y_del = lead_x_del

                elif event.key == pygame.K_UP:
                    print "This is K_UP"
                    if lead_y_del != block_size:
                        lead_y_del = -block_size
                        lead_x_del = 0
                        
                    if mods & pygame.KMOD_CTRL:
                        print "UP + CTRL pressed :D"
                        if (lead_x_del != -block_size) or (lead_y_del != block_size):
                            lead_x_del = block_size
                            lead_y_del = -lead_x_del

                elif event.key == pygame.K_DOWN:
                    print "This is K_DOWN"
                    if lead_y_del != -block_size:
                        lead_y_del = block_size
                        lead_x_del = 0
                    if mods & pygame.KMOD_CTRL:
                        print "Down + CTRL pressed :D"
                        if (lead_x_del != block_size) or (lead_y_del != -block_size):
                            lead_x_del = -block_size
                            lead_y_del = -lead_x_del

                elif event.key == pygame.K_a: # in this elif I will check for CTRL key pressed or not :D
                    mods = pygame.key.get_mods()        # Assining a name, to use easily :D

                    if mods & pygame.KMOD_CTRL:
                        print "a + CTRL pressed :D"
                    else:
                        print "Only a is pressed :D"

                # elif event.key == pygame.K_RCTRL: # This is for special R_CTRL key :D
                #     print "Inside the K_RCTRL loop :D"
                    
                print (prev_key,event.key)             # To print out the KEY related to buttons on screen :D
                # Strictly at the end the if loop of event.type :D
                prev_key = event.key        # Maintain a prev state, this will be used in program :D
                
        if lead_x >= dispWidth or lead_x < 0 or lead_y >= dispHeight or lead_y < 0:
            gameOver = True
        lead_x += lead_x_del
        lead_y += lead_y_del

        print (lead_x_del,lead_y_del) # To see what are the values are being added or subtrached :D

        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, block_size, block_size])
        
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachElem in snakeList[:-1]:
            if eachElem == snakeHead:
                gameOver = True

        snake(block_size, snakeList)
        pygame.display.update()

        if lead_x == randAppleX and lead_y == randAppleY:
            randAppleX = round(random.randrange(0, dispWidth - block_size)/10.0)*10
            randAppleY = round(random.randrange(0, dispHeight - block_size)/10.0)*10
            snakeLength += 1
        
        clock.tick(FPS)
    pygame.quit()
    print "++++-----------------------------------++++"
    quit()

gameLoop()
