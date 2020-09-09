##
# A small pygame program that displays a circle on a screen. 
# Detects when the user has clicked within a circle
#
# Authors: Nicholas O'Kelley, Daniel Hammer, Brandon Moore
# Date: Feb. 20 2020
##

import pygame
import random
import math

global screen

# Global constants
RADIUS = 50
THICKNESS = 5
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
DISTANCE_APART = 175
HELP_X, HELP_Y = 100, 100
NUM_VERTICES = 7

# Color dictionary, (Red,Green,Blue,Alpha)
CRAYONBOX = {
        "WHITE": (255,255,255,255),
        "BLACK": (0,0,0,255),
        "BLUE": (0,0,255,255),
        "RED": (255,0,0,255),
        "GREEN":(0,255,0,255),
        "YELLOW":(255,255,0,255),
        "PINK":(255,0,255,255),
        "CYAN":(0,255,255,255),
        }

VERTICES = []




def main():
    # The background color that sets the R,G,B colors to white
    background_color = (255, 255, 255)
    
    # The screen variable that sets display using the width and height variables
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Sets the title bar of the screen
    pygame.display.set_caption('Building a Circle')

    # Fills the screen with the color
    screen.fill(background_color)

    # This command udpates the whole screen 
    pygame.display.flip()

    # Create a path of n vertices on screen
    create_graph(screen, NUM_VERTICES)
    pygame.display.update()

    # Run until false
    running = True
    while running:

        # Will update to false when the user clicks the X
        event = pygame.event.get()
        for event in event:

            # Get all mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Store the click position's coordinates
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check the x,y for every vertex on screen
                for vtx in VERTICES:
                    circle_x = list(vtx.keys())[0]
                    circle_y = vtx.get(circle_x)

                    # If the circle was clicked, print true
                    if (is_clicked(circle_x, circle_y, mouse_x, mouse_y, RADIUS)):
                        keys = pygame.key.get_pressed()
                        recolor(screen, RADIUS, keys, circle_x, circle_y)

                pygame.display.update()

            # If the window is closed, exit the game
            if event.type == pygame.QUIT:
                running = False




# Creates a graph with the provided number of vertices
def create_graph(screen, number_of_vertices):
    """
    Creates a standard path of n vertices on screen

    Creates a circle to keep track of the last color played
    Creates a vertex spaced DISTANCE_APART pixels apart at the
        middle height of the screen
    Draws lines connecting each vertex
    Saves a dictionary of each vertex's center

    Parameters:
    screen (pygame object): The game window
    number_of_vertices (int): The number of vertices to draw

    Returns:
    N/A
    """

    pygame.draw.circle(screen, CRAYONBOX["BLACK"], (HELP_X, HELP_Y), 30, 5)

    for i in range(0, number_of_vertices):
        x = i*DISTANCE_APART + 100
        y = int(WINDOW_HEIGHT / 2)

        pygame.draw.circle(screen, CRAYONBOX["BLACK"], (x, y), RADIUS, THICKNESS)
        VERTICES.append({x:y})
        if i is not number_of_vertices - 1:
            pygame.draw.line(screen, CRAYONBOX["BLACK"], (x + RADIUS, y), (x + DISTANCE_APART - RADIUS, y), THICKNESS)

    #print(VERTICES)




# Checks to see if the mouse was within a specified radius
def is_clicked(circle_x, circle_y, mouse_x, mouse_y, radius):
    """
    Determines whether or not the user clicked within a vertex

    Parameters:
    circle_x (int): The vertex's center's x coordinate
    circle_y (int): The vertex's center's y coordinate
    mouse_x (int): The mouse click's x coordinate
    mouse_y (int): The mouse click's y coordinate

    Returns:
    True if the user clicked within the vertex, else false
    """
    return math.sqrt(((mouse_x - circle_x) ** 2) + ((mouse_y - circle_y) ** 2)) < radius




# Recolor the circle
# Based on what key was pressed
# Also tracks the most recent color played
def recolor(screen, radius, keys, circle_x, circle_y):
    """
    Recolors a vertex

    Gets the current color of the vertex
    Sets the new color according to what key was pressed
    If the new color is not the old color, recolor the vertex
    Also recolor the last-color-used display

    Parameters:
    screen (pygame object): The game window
    radius (int): Radius of a vertex in pixels
    keys (boolean array): List of the state of all keyboard keys
    circle_x (int): The vertex's center's x coordinate
    circle_y (int): The vertex's center's y coordinate

    Returns:
    N/A

    """
    current_color = screen.get_at((circle_x, circle_y))
    if keys[pygame.K_1]:
        new_color = "BLUE"
    elif keys[pygame.K_2]:
        new_color = "GREEN"
    elif keys[pygame.K_3]:
        new_color = "RED"
    elif keys[pygame.K_4]:
        new_color = "YELLOW"
    elif keys[pygame.K_5]:
        new_color = "PINK"
    elif keys[pygame.K_6]:
        new_color = "CYAN"
    else:
        return

    if CRAYONBOX[new_color] != current_color:
        pygame.draw.circle(screen, CRAYONBOX[new_color], (circle_x, circle_y), radius - 5)
        pygame.draw.circle(screen, CRAYONBOX[new_color], (HELP_X, HELP_Y), 25)




if __name__ == '__main__':
    main()
