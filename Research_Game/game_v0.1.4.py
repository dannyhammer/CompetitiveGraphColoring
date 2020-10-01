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
        - The create_cycle() function's adjacency section is ugly

    Graphic overhaul!
        This game is incredibly basic and ugly. It needs a UI overhaul.
        Elements such as an input box, player turn display, win/lose screen, etc.
        all need to be developed to make the game more appealing.
        - Text boxes to display game controls
        - Player 1/2 names and last-color-used displays need text as well

    Radius tweaks.
        Set the radius and thickness to be inversely proportional to the number
        of vertices entered.

    Menu selection.
        In order to change graph types right now, you have to manually edit
        TYPE_OF_GRAPH (1-path, 2-cycle, 3-custom). We need a selection menu
        to allow users to select what kind of graph to play on.
"""

import pygame
import random
import math

# Global constants
RADIUS = 30
THICKNESS = 5
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
TEXT_BOX_WIDTH = 140
TEXT_BOX_HEIGHT = 32
P1_LAST_X, P1_LAST_Y = 100, 100
P2_LAST_X, P2_LAST_Y = WINDOW_WIDTH - 100, 100
VERTICES = []
TYPE_OF_GRAPH = 2

# Determines what you can input in the num_vertices selection box
VALID_INPUTS = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
        pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9,
        pygame.K_ESCAPE, pygame.K_BACKSPACE, pygame.K_RETURN]

# Color dictionary, (Red,Green,Blue,Alpha)
CRAYONBOX = {
        "WHITE": (255,255,255,255),
        "BLACK": (0,0,0,255),
        "BLUE": (0,0,255,255),
        "RED": (255,0,0,255),
        "GREEN": (0,255,0,255),
        "YELLOW": (255,255,0,255),
        "PINK": (255,0,255,255),
        "CYAN": (0,255,255,255),
        "GRAY": (169,169,169,255),
        }
BACKGROUND = CRAYONBOX["GRAY"];



def main():
    pygame.init()
    pygame.font.init()
    
    # The screen variable that sets display using the width and height variables
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Sets the title bar of the screen
    pygame.display.set_caption(__file__)

    # Fills the screen with the color
    screen.fill(BACKGROUND)




    # This defines the text input box boundaries
    input_box = pygame.Rect(WINDOW_WIDTH / 2 - (TEXT_BOX_WIDTH / 2), WINDOW_HEIGHT / 4 - TEXT_BOX_HEIGHT / 2, TEXT_BOX_WIDTH, TEXT_BOX_HEIGHT)

    # Colors for the box on whether it is active or not
    color_inactive = CRAYONBOX["CYAN"]
    color_active = CRAYONBOX["BLUE"]

    # default coloring of box
    text_box_color = color_inactive

    #define a quick font
    font = pygame.font.Font(None, 32)

    # Box and game are both active to begin with
    active = True
    game_running = True

    #default box value is blank
    text_input = ''
    

    # If the graph is a custom graph, give default values and skip setup
    setup_running = False if TYPE_OF_GRAPH is 3 else True
    num_vertices = 0 if TYPE_OF_GRAPH is 3 else True

    # Setup Window
    while setup_running:

        for event in pygame.event.get():

            # Get all mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Toggle the input box's activity
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                #change the color of the input box
                text_box_color = color_active if active else color_inactive

            # Give the text box some font
            txt_surface = font.render(text_input, True, CRAYONBOX["BLACK"])

            # Draw the input box
            input_box.w = max(200, txt_surface.get_width() + 10)
            pygame.draw.rect(screen, text_box_color, input_box, 3)
            pygame.draw.rect(screen, CRAYONBOX["WHITE"], input_box)
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

            if event.type == pygame.KEYDOWN:

                # Get all keys pressed
                keys = pygame.key.get_pressed()

                # If the text box is active and the text input is valid
                if active and event.key in VALID_INPUTS:

                    # Submit the inputted text
                    if event.key == pygame.K_RETURN:
                        num_vertices = int(text_input);
                        active = False
                        setup_running = False

                    # Decrement the text input
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]

                        pygame.draw.rect(screen, CRAYONBOX["WHITE"], input_box)
                        txt_surface = font.render(text_input, True, text_box_color)
                        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

                    # Add to text input
                    else:
                        text_input += event.unicode

                # Close window on pressing ESC
                if event.key == pygame.K_ESCAPE:
                    setup_running = False
                    game_running = False


            # If the window is closed, exit the game
            if event.type == pygame.QUIT:
                setup_running = False
                game_running = False

            pygame.display.update()




    # Create a graph
    screen.fill(BACKGROUND)
    create_graph(screen, num_vertices, RADIUS, THICKNESS, TYPE_OF_GRAPH)
    pygame.display.update()




    # Game loop
    while game_running:

        for event in pygame.event.get():

            # Get all mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Store the click position's coordinates
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # If the circle was clicked, recolor it
                for vtx in VERTICES:
                    if (is_clicked(vtx["x"], vtx["y"], mouse_x, mouse_y, RADIUS)):
                        recolor(screen, RADIUS, pygame.key.get_pressed(), vtx["x"], vtx["y"])

            if event.type == pygame.KEYDOWN:

                # Get all keys pressed
                keys = pygame.key.get_pressed()

                # Reset the game upon pressing 'r'
                if event.key == pygame.K_r:
                    reset_game(screen, RADIUS, THICKNESS)

                # Close window on pressing ESC
                if event.key == pygame.K_ESCAPE:
                    game_running = False

            # If the window is closed, exit the game
            if event.type == pygame.QUIT:
                game_running = False

            pygame.display.update()









def create_path(screen, number_of_vertices, radius, thickness):
    """
    Creates a standard path of n vertices on screen

    Creates a circle to keep track of the last color played
    Creates a vertex spaced dist_apart pixels apart at the
        middle height of the screen
    Draws lines connecting each vertex
    Saves a dictionary of each vertex's center

    Parameters:
    screen (pygame object): The game window
    number_of_vertices (int): The number of vertices to draw
    radius (int): The radius of a vertex
    thickness (int): the thickness of a vertex's outer ring

    Returns:
    N/A
    """

    dist_apart = radius * 3

    for i in range(0, number_of_vertices):
        vtx_x = i*dist_apart + int((WINDOW_WIDTH - dist_apart * (number_of_vertices - 1)) / 2)
        vtx_y = int(WINDOW_HEIGHT / 2)

        vtx = {"ID": i,
                "x": vtx_x,
                "y": vtx_y,
                "color": "WHITE",
                "adjacent": [],
                }

        VERTICES.append(vtx);

        # Connect each vertex with a line
        if i is not number_of_vertices - 1:
            pygame.draw.line(screen, CRAYONBOX["BLACK"], (vtx_x, vtx_y), (vtx_x + dist_apart, vtx_y), thickness)

    # Assign adjacency
    for i in range(0, number_of_vertices):
        pygame.draw.circle(screen, CRAYONBOX["BLACK"], (VERTICES[i]["x"], VERTICES[i]["y"]), radius, thickness)
        pygame.draw.circle(screen, CRAYONBOX["WHITE"], (VERTICES[i]["x"], VERTICES[i]["y"]), radius - thickness)

        if i is not 0:
            VERTICES[i]["adjacent"].append(VERTICES[i - 1]["ID"])
        if i is not number_of_vertices - 1:
            VERTICES[i]["adjacent"].append(VERTICES[i + 1]["ID"])




def create_cycle(screen, number_of_vertices, radius, thickness):
    """
    Creates a standard cycle of n vertices on screen

    Creates a circle to keep track of the last color played
    Creates a vertex spaced dist_apart pixels apart at the
        middle height of the screen
    Draws lines connecting each vertex
    Saves a dictionary of each vertex's center

    Parameters:
    screen (pygame object): The game window
    number_of_vertices (int): The number of vertices to draw
    radius (int): The radius of a vertex
    thickness (int): the thickness of a vertex's outer ring

    Returns:
    N/A
    """

    dist_apart = number_of_vertices * 15

    for i in range(0, number_of_vertices):
        vtx_x = int((WINDOW_WIDTH / 2) + math.cos((i * math.pi * 2)/number_of_vertices) * dist_apart)
        vtx_y = int((WINDOW_HEIGHT / 2) + math.sin((i * math.pi * 2)/number_of_vertices) * dist_apart)

        vtx = {"ID": i,
                "x": vtx_x,
                "y": vtx_y,
                "color": "WHITE",
                "adjacent": [],
                }

        VERTICES.append(vtx);

    # Assign adjacency
    for i in range(0, number_of_vertices):
        if i is not 0:
            VERTICES[i]["adjacent"].append(VERTICES[i - 1]["ID"])
        else: 
            VERTICES[i]["adjacent"].append(VERTICES[number_of_vertices - 1]["ID"])

        if i is not number_of_vertices - 1:
            VERTICES[i]["adjacent"].append(VERTICES[i + 1]["ID"])
            pygame.draw.line(screen, CRAYONBOX["BLACK"], (VERTICES[i]["x"], VERTICES[i]["y"]), (VERTICES[i + 1]["x"], VERTICES[i + 1]["y"]), thickness)
        else:
            VERTICES[i]["adjacent"].append(VERTICES[0]["ID"])
            pygame.draw.line(screen, CRAYONBOX["BLACK"], (VERTICES[i]["x"], VERTICES[i]["y"]), (VERTICES[0]["x"], VERTICES[0]["y"]), thickness)

    # Display the vertices
    for i in range(0, number_of_vertices):
        pygame.draw.circle(screen, CRAYONBOX["BLACK"], (VERTICES[i]["x"], VERTICES[i]["y"]), radius, thickness)
        pygame.draw.circle(screen, CRAYONBOX["WHITE"], (VERTICES[i]["x"], VERTICES[i]["y"]), radius - thickness)


def create_custom_graph(screen, radius, thickness):
    """
    Generates a custom-made graph

    The users clicks while pressing 'v' to create a vertex. Clicking and
    dragging will create an edge between two vertices. Pressing 'c' will create
    the graph and begin the game.

    Parameters:
    screen (pygame object): The game window
    radius (int): The radius of a vertex
    thickness (int): the thickness of a vertex's outer ring

    Returns:
    N/A
    """

    generating = True

    # Number of vertices created and the two vertices to connect
    vertices_created = 0
    vtx_one = None
    vtx_two = None

    while generating:

        for event in pygame.event.get():

            # Get all mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Store the click position's coordinates
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Get all keys pressed
                keys = pygame.key.get_pressed()

                # Create a vertex when clicking and pressing 'v'
                if keys[pygame.K_v]:
                    vtx = {"ID": vertices_created,
                            "x": mouse_x,
                            "y": mouse_y,
                            "color": "WHITE",
                            "adjacent": [],
                            }
                    VERTICES.append(vtx);
                    vertices_created += 1
                    pygame.draw.circle(screen, CRAYONBOX["BLACK"], (mouse_x, mouse_y), radius, thickness)
                    pygame.draw.circle(screen, CRAYONBOX["WHITE"], (mouse_x, mouse_y), radius - thickness)

                # Set the source vertex to whichever vertex was clicked on
                for vtx in VERTICES:
                    if (is_clicked(vtx["x"], vtx["y"], mouse_x, mouse_y, RADIUS)):
                        vtx_one = vtx
                    
            if event.type == pygame.MOUSEBUTTONUP:

                # Store the click position's coordinates
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Set the destination vertex to whichever vertex was under the
                # cursor after the click
                for vtx in VERTICES:
                    if (is_clicked(vtx["x"], vtx["y"], mouse_x, mouse_y, RADIUS)):
                        vtx_two = vtx

                # If the source and destination vertices have values, connect them
                if vtx_one is not None and vtx_two is not None:
                    pygame.draw.line(screen, CRAYONBOX["BLACK"], (vtx_one["x"], vtx_one["y"]), (vtx_two["x"], vtx_two["y"]), thickness)
                    pygame.draw.circle(screen, CRAYONBOX["WHITE"], (vtx_one["x"], vtx_one["y"]), radius - thickness)
                    pygame.draw.circle(screen, CRAYONBOX["WHITE"], (vtx_two["x"], vtx_two["y"]), radius - thickness)
                    vtx_one["adjacent"].append(vtx_two["ID"])
                    vtx_two["adjacent"].append(vtx_one["ID"])
                    


            if event.type == pygame.KEYDOWN:

                # Reset the graph generation if 'r' is pressed
                if event.key == pygame.K_r:
                    vertices_created = 0
                    VERTICES.clear()
                    vtx_one = None
                    vtx_two = None
                    screen.fill(BACKGROUND)

                # Close window on pressing ESC
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_c:
                    generating = False

            # If the window is closed, exit the game
            if event.type == pygame.QUIT:
                generating = False

            pygame.display.update()









def create_graph(screen, number_of_vertices, radius, thickness, choice):
    """
    Determines what graph to display based on input

    Parameters:
    screen (pygame object): The game window
    number_of_vertices (int): The number of vertices to draw
    radius (int): The radius of a vertex
    thickness (int): the thickness of a vertex's outer ring
    choice (int): The graph to generate

    Returns:
    N/A
    """
    if choice is 1:
        create_path(screen, number_of_vertices, radius, thickness)
    elif choice is 2:
        create_cycle(screen, number_of_vertices, radius, thickness)
    elif choice is 3:
        create_custom_graph(screen, radius, thickness)

    pygame.draw.circle(screen, CRAYONBOX["BLACK"], (P1_LAST_X, P1_LAST_Y), 30, 5)
    pygame.draw.circle(screen, CRAYONBOX["WHITE"], (P1_LAST_X, P1_LAST_Y), 25)
    pygame.draw.circle(screen, CRAYONBOX["BLACK"], (P2_LAST_X, P2_LAST_Y), 30, 5)
    pygame.draw.circle(screen, CRAYONBOX["WHITE"], (P2_LAST_X, P2_LAST_Y), 25)




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




def reset_game(screen, radius, thickness):
    """
    Resets the game

    Recolors all vertices on screen to white, including the last color used slot

    Parameters:
    screen (pygame object): The game window
    radius (int): The radius of each vertex

    Returns:
    N/A
    """
    pygame.draw.circle(screen, CRAYONBOX["WHITE"], (P1_LAST_X, P1_LAST_Y), 25)
    pygame.draw.circle(screen, CRAYONBOX["WHITE"], (P2_LAST_X, P2_LAST_Y), 25)
    for vtx in VERTICES:
        pygame.draw.circle(screen, CRAYONBOX["WHITE"], (vtx["x"], vtx["y"]), radius - thickness)




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
        pygame.draw.circle(screen, CRAYONBOX[new_color], (P1_LAST_X, P1_LAST_Y), 25)
        pygame.draw.circle(screen, CRAYONBOX[new_color], (P2_LAST_X, P2_LAST_Y), 25)
        vertex["color"] = new_color




if __name__ == '__main__':
    main()
