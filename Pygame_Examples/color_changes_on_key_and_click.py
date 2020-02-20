##
# A small pygame program that displays a circle on a screen. 
# Detects when the user has clicked within a circle
#
# Authors: Nicholas O'Kelley, Daniel Hammer 
# Date: Feb. 13 2020
##

import pygame
import random
import math

global screen
global running
global num_vertices

RADIUS = 25
THICKNESS = 5
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Color dictionary, R G B
CRAYONBOX = {
        "BLACK": (0,0,0,255),
        "BLUE": (0,0,255,255),
        "RED": (255,0,0,255),
        "GREEN":(0,255,0,255),
        "YELLOW":(255,255,0,255),
        "PINK":(255,0,255,255),
        "CYAN":(0,255,255,255),
        }

VERTICES = []
"""
VERTICES = {
        INDEX: (x, y) // center
        }
"""

def main():
    # The background color that sets the R,G,B colors to white
    background_color = (255, 255, 255)
    
    num_vertices = 12

    # The screen variable that sets display using the width and height variables
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Sets the title bar of the screen
    pygame.display.set_caption('Building a Circle')

    # Fills the screen with the color
    screen.fill(background_color)

    # This command udpates the whole screen 
    pygame.display.flip()

    # Boolean for the state of the program
    running = True


    create_graph(screen, num_vertices)
    pygame.display.update()
    # Run until false
    num_vertices = 0
    while running:

        event = pygame.event.get()

        # Will update to false when the user clicks the X
        for event in event:

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check the x,y for every vertex on screen
                for vtx in VERTICES:
                    for circle_x, circle_y in vtx.items():
                        # If the circle was clicked, print true
                        if (is_clicked(circle_x, circle_y, mouse_x, mouse_y, RADIUS)):
                            keys = pygame.key.get_pressed()
                            recolor(screen, RADIUS, keys, circle_x, circle_y)
                pygame.display.update()

            if event.type == pygame.QUIT:
                running = False

# Creates a graph with the provided number of vertices
def create_graph(screen, number_of_vertices):
    for i in range(0, number_of_vertices):
        x = i*100 + 100
        y = int(WINDOW_HEIGHT / 2)

        pygame.draw.circle(screen, CRAYONBOX["BLACK"], (x, y), RADIUS, THICKNESS)
        VERTICES.append({x:y})
    #print(VERTICES)

# Checks to see if the mouse was within a specified radius
def is_clicked(circle_x, circle_y, mouse_x, mouse_y, radius):
    return math.sqrt(((mouse_x - circle_x) ** 2) + ((mouse_y - circle_y) ** 2)) < radius

# Recolor the circle
# Based on what key was pressed
def recolor(screen, radius, keys, circle_x, circle_y):
    current_color = screen.get_at((circle_x, circle_y))
    print(current_color)
    if keys[pygame.K_1]:
        pygame.draw.circle(screen, CRAYONBOX["BLUE"], (circle_x, circle_y), radius - 5)
    elif keys[pygame.K_2]:
        pygame.draw.circle(screen, CRAYONBOX["GREEN"], (circle_x, circle_y), radius - 5)
    elif keys[pygame.K_3]:
        pygame.draw.circle(screen, CRAYONBOX["RED"], (circle_x, circle_y), radius - 5)
    elif keys[pygame.K_4]:
        pygame.draw.circle(screen, CRAYONBOX["YELLOW"], (circle_x, circle_y), radius - 5)
    elif keys[pygame.K_5]:
        pygame.draw.circle(screen, CRAYONBOX["PINK"], (circle_x, circle_y), radius - 5)
    elif keys[pygame.K_6]:
        pygame.draw.circle(screen, CRAYONBOX["CYAN"], (circle_x, circle_y), radius - 5)


if __name__ == '__main__':
    main()
