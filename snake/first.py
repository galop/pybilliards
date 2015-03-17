#!/usr/bin/python

import pygame
pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption('theVault')
clock = pygame.time.Clock()

lead_x = 300
lead_y = 300
x_size = 10
movement_smoothness = 2
lead_x_del = 0
lead_y_del = 0
pygame.display.update()

gameExit = False

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                lead_x_del = -movement_smoothness
                lead_y_del = 0
            elif event.key == pygame.K_RIGHT:
                lead_x_del = movement_smoothness
                lead_y_del = 0
            elif event.key == pygame.K_UP:
                lead_y_del = -movement_smoothness
                lead_x_del = 0
            elif event.key == pygame.K_DOWN:
                lead_y_del = movement_smoothness
                lead_x_del = 0

    lead_x += lead_x_del
    lead_y += lead_y_del

    gameDisplay.fill(white)
    pygame.draw.rect(gameDisplay, black, [lead_x, lead_y, x_size, 10])
#   gameDisplay.fill(blue, rect=[200,200,50,50])
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
