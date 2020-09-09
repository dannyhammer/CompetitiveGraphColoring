##
# A small pygame program that displays a circle on a screen. 
# Detects when the user has clicked within a circle
#
# Authors: Nicholas O'Kelley, Daniel Hammer, Brandon Moore
# Date: Feb. 20 2020
##

"""

TODO:

    Assign colors to each vertex object.
        Right now, only the screen is being recolored. We need to reassign the
        'color' field of a vertex object concurrently with its corresponding
        location on screen. This can be done by accessing each vertex's 'x' and
        'y' fields and mutating the 'color' field alongside the screen in the
        recolor method.

    Write a function to determine legal coloring.
        This can be a subset of the recolor method if needed. All that needs
        to be done is check the 'color' field of every vertex in a given
        vertex's 'adjacent' field and checking their corresponding colors
        alongside the provided color.

    Write more graphs. [NOT A PRIORITY]
        We create paths right now, and that exists as the entirety of the
        'create_graph' function. Repurpose this function to call other functions
        that create path, cycle, and other graphs as needed.
"""

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
    create_graph(screen, NUM_VERTICES, RADIUS, THICKNESS)
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
                    #vtx_x = list(vtx.keys())[0]
                    #vtx_y = vtx.get(vtx_x)
                    vtx_x = vtx["x"]
                    vtx_y = vtx["y"]

                    # If the circle was clicked, print true
                    if (is_clicked(vtx_x, vtx_y, mouse_x, mouse_y, RADIUS)):
                        keys = pygame.key.get_pressed()
                        recolor(screen, RADIUS, keys, vtx_x, vtx_y)


            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if event.key == pygame.K_r:
                    reset_game(screen, RADIUS)


            # If the window is closed, exit the game
            if event.type == pygame.QUIT:
                running = False

            pygame.display.update()



# Creates a graph with the provided number of vertices
def create_graph(screen, number_of_vertices, radius, thickness):
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
        vtx_x = i*DISTANCE_APART + 100
        vtx_y = int(WINDOW_HEIGHT / 2)
        pygame.draw.circle(screen, CRAYONBOX["BLACK"], (vtx_x, vtx_y), radius, thickness)

        vtx = {"ID": i,
                "x": vtx_x,
                "y": vtx_y,
                "color": "WHITE",
                "adjacent": [],
                }
        pygame.draw.circle(screen, CRAYONBOX["WHITE"], (vtx_x, vtx_y), radius - 5)

        VERTICES.append(vtx);

        if i is not number_of_vertices - 1:
            pygame.draw.line(screen, CRAYONBOX["BLACK"], (vtx_x + radius, vtx_y), (vtx_x + DISTANCE_APART - radius, vtx_y), thickness)
    for i in range(0, number_of_vertices):
        if i is not 0:
            VERTICES[i]["adjacent"].append(VERTICES[i - 1]["ID"])
        if i is not number_of_vertices - 1:
            VERTICES[i]["adjacent"].append(VERTICES[i + 1]["ID"])

    #print(VERTICES)
    for vtx in VERTICES:
        print("vertex " + str(vtx["ID"]) + " is adjacent with " + str(vtx["adjacent"]))
        print(vtx["color"])




# Checks to see if the mouse was within a specified radius
def is_clicked(vtx_x, vtx_y, mouse_x, mouse_y, radius):
    """
    Determines whether or not the user clicked within a vertex

    Parameters:
    vtx_x (int): The vertex's center's x coordinate
    vtx_y (int): The vertex's center's y coordinate
    mouse_x (int): The mouse click's x coordinate
    mouse_y (int): The mouse click's y coordinate

    Returns:
    True if the user clicked within the vertex, else false
    """
    return math.sqrt(((mouse_x - vtx_x) ** 2) + ((mouse_y - vtx_y) ** 2)) < radius


def reset_game(screen, radius):
    """
    Resets the game

    Recolors all vertices on screen to white, including the last color used slot

    Parameters:
    screen (pygame object): The game window
    radius (int): The radius of each vertex

    Returns:
    N/A
    """
    pygame.draw.circle(screen, CRAYONBOX["WHITE"], (HELP_X, HELP_Y), 25)
    for vtx in VERTICES:
        pygame.draw.circle(screen, CRAYONBOX["WHITE"], (vtx["x"], vtx["y"]), radius - 5)



# Recolor the circle
# Based on what key was pressed
# Also tracks the most recent color played
def recolor(screen, radius, keys, vtx_x, vtx_y):
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
    vtx_x (int): The vertex's center's x coordinate
    vtx_y (int): The vertex's center's y coordinate

    Returns:
    N/A

    """
    current_color = screen.get_at((vtx_x, vtx_y))
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
        pygame.draw.circle(screen, CRAYONBOX[new_color], (vtx_x, vtx_y), radius - 5)
        pygame.draw.circle(screen, CRAYONBOX[new_color], (HELP_X, HELP_Y), 25)

"""
def make_vertex(screen, radius, vtx_id, vtx_x, vtx_y):
    vtx = {ID: vtx_id,
            x: vtx_x,
            y: vtx_y,
            color: "WHITE",
            adjacent: [],
            }
    pygame.draw.circle(screen, CRAYONBOX[new_color], (vtx_x, vtx_y), radius - 5)
    VERTICES.append(vtx);
"""



if __name__ == '__main__':
    main()
