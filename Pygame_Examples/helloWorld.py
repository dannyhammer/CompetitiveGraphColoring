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

input("Enter anything ... ")
