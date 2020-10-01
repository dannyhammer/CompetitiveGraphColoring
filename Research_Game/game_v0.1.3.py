##
# A small pygame program that displays a circle on a screen. 
# Detects when the user has clicked within a circle
#
# Authors: Nicholas O'Kelley, Daniel Hammer, Brandon Moore
# Date: Feb. 22 2020
##

"""

TODO:

    Refactor.
        Things like global constants need to be restructured. The 'screen'
        variable is passed in to almost every function, so it should probably
        be global. Constants should probably be specified and restructured as
        well.

    Write more graphs. [NOT A PRIORITY]
        We create paths right now, and that exists as the entirety of the
        'create_graph' function. Repurpose this function to call other functions
        that create path, cycle, and other graphs as needed.

    Graphic overhaul!
        This game is incredibly basic and ugly. It needs a UI overhaul.
        Elements such as an input box, player turn display, win/lose screen, etc.
        all need to be developed to make the game more appealing.
"""

import pygame
from pygame.locals import *
import random
import math

# Global constants
RADIUS = 50
THICKNESS = 5
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
DISTANCE_APART = 175
HELP_X, HELP_Y = 100, 100
NUM_VERTICES = 7
VERTICES = []

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





def main():
    pygame.init()

    pygame.font.init()
    # The background color that sets the R,G,B colors to white
    background_color = (169,169,169)
    
    # The screen variable that sets display using the width and height variables
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Sets the title bar of the screen
    pygame.display.set_caption('game_v0.1.3.py')

    # Fills the screen with the color
    screen.fill(background_color)

    # This command udpates the whole screen 
    pygame.display.flip()

    # Create a path of n vertices on screen
    create_graph(screen, NUM_VERTICES, RADIUS, THICKNESS)
    pygame.display.update()

    # This defines the box boundary
    input_box = pygame.Rect(500, 100,140, 32)

    # Colors for the box on whether it is active or not
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')

    # default coloring of box
    color = color_inactive

    #define a quick font
    font = pygame.font.Font(None, 32)

    # box is not active to begin with
    active = False
    
    #default box value is blank
    text_input = ''
    

    # Run until false
    running = True
    while running:

        # Will update to false when the user clicks the X
        event = pygame.event.get()
        for event in event:

            if event.type == pygame.MOUSEBUTTONDOWN:
                #click in the box, do this
                if input_box.collidepoint(event.pos):
                    #toggle active var
                    active = not active
                else:
                    active = False
                #change the color of the input box
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text_input)
                        text_input = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode


            txt_surface = font.render(text_input, True, color)

            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

            pygame.draw.rect(screen, color, input_box, 2)
        

            # Get all mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Store the click position's coordinates
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check the x,y for every vertex on screen
                for vtx in VERTICES:
                    vtx_x = vtx["x"]
                    vtx_y = vtx["y"]

                    # If the circle was clicked, print true
                    if (is_clicked(vtx_x, vtx_y, mouse_x, mouse_y, RADIUS)):
                        keys = pygame.key.get_pressed()
                        recolor(screen, RADIUS, keys, vtx_x, vtx_y)
                    #print(vtx["color"])


            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if event.key == pygame.K_r:
                    reset_game(screen, RADIUS)


            # If the window is closed, exit the game
            if event.type == pygame.QUIT:
                running = False

            pygame.display.update()



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




def is_legal(vtx, color):
    """
    Checks if a coloring is legal

    Loops through the vertex's neighbors and compares their colors to the
    proposed new color. If any of the neighbors are already colored with the
    proposed new color, a coloring cannot be completed

    Parameters:
    vtx (dictionary): The vertex attempting to be colored
    color (string): The proposed new color

    Returns:
    True if no neighbors are already colored with the proposed new color
    False if any neighbor is already colored with the proposed new color
    """
    for neighbor in vtx["adjacent"]:
        if VERTICES[neighbor]["color"] is color:
            return False
    return True




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

    vertex = {}
    for vtx in VERTICES:
        if vtx["x"] == vtx_x and vtx["y"] == vtx_y:
            vertex = vtx

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

    if CRAYONBOX[new_color] != current_color and is_legal(vertex, new_color):
        pygame.draw.circle(screen, CRAYONBOX[new_color], (vtx_x, vtx_y), radius - 5)
        pygame.draw.circle(screen, CRAYONBOX[new_color], (HELP_X, HELP_Y), 25)
        vertex["color"] = new_color




if __name__ == '__main__':
    main()
