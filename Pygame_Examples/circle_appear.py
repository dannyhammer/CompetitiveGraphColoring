##
# A small pygame program that displays a circle on a screen. 
#
# Author: Nicholas O'Kelley 
# Date: Feb. 6th 2020
##

import pygame

global screen
global running
BLACK = (0, 0, 0)

def main():
    # The background color that sets the R,G,B colors to white
    background_color = (255, 255, 255)

    # The width variable
    width = 640
    # The height variable
    height = 480

    # The screen variable that sets display using the width and height variables
    screen = pygame.display.set_mode((width, height))

    # Sets the title bar of the screen
    pygame.display.set_caption('Building a Circle')

    # Fills the screen with the color
    screen.fill(background_color)

    # This command udpates the whole screen 
    pygame.display.flip()

    # Boolean for the state of the program
    running = True


    # Run until false
    while running:

        event = pygame.event.get()

        # Will update to false when the user clicks the X
        for event in event:

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.circle(screen, BLACK, (150, 200), 25, 5)
                pygame.display.update()


            if event.type == pygame.QUIT:
                running = False

if __name__ == '__main__':
    main()
