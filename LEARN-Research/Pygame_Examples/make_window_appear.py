##
# A small program setting up a window
#
# Author Nicholas O'Kelley
##

import pygame

# Initialize pygame
pygame.init()

# Set up the window
window = pygame.display.set_mode((500,400), 0, 32)

# Sets the windows "header"
pygame.display.set_caption('Hello World!')

# boolean for the state of the program
running = True

# Keep the program running until you click the X button
while running:

    # How the program evaluates if the X button was clicked
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
