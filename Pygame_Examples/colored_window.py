##
# A small pygame program that opens a a colored window. 
#
# Author: Nicholas O'Kelley 
# Date: Feb. 6th 2020
##

import pygame

# The background color that sets the R,G,B colors to white
background_color = (255, 255, 255)

# The width variable
width = 300
# The height variable
height = 200

# The window variable that sets display using the width and height variables
window = pygame.display.set_mode((width, height))

# Sets the title bar of the window
pygame.display.set_caption('Colored Windows are Cool')

# Fills the screen with the color
window.fill(background_color)

# This command udpates the whole window 
pygame.display.flip()

# Boolean for the state of the program
running = True

# Run until false
while running:

    # Will update to false when the user clicks the X
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
