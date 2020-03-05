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
        - A draw_graph() function should be called whenever the screen needs to be
            updated when creating a graph, allowing users to delete and reorder
            vertices and edges.

    Graphic overhaul!
        This game is incredibly basic and ugly. It needs a UI overhaul.
        Elements such as an input box, player turn display, win/lose screen, etc.
        all need to be developed to make the game more appealing.
        - Text boxes to display game controls

    Menu selection.
        In order to change graph types right now, you have to manually edit
        TYPE_OF_GRAPH (1-path, 2-cycle, 3-custom). We need a selection menu
        to allow users to select what kind of graph to play on.

"""

import pygame
import random
import math

# Global constants
RADIUS = 35
THICKNESS = int(RADIUS / 6)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
TEXT_BOX_WIDTH = 140
TEXT_BOX_HEIGHT = 32
VERTICES = []
TYPE_OF_GRAPH = 2

# Determines what you can input in the num_vertices selection box
VALID_INPUTS = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
        pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9,
        pygame.K_ESCAPE, pygame.K_BACKSPACE, pygame.K_RETURN]

# Color dictionary, (Red,Green,Blue,Alpha)
CRAYONBOX = {
        "WHITE": (255,255,255,255),
        "GRAY": (169,169,169,255),
        "BLACK": (0,0,0,255),
        "BLUE": (0,0,255,255),
        "RED": (255,0,0,255),
        "GREEN": (0,255,0,255),
        "YELLOW": (255,255,0,255),
        "PINK": (255,0,255,255),
        "CYAN": (0,255,255,255),
        "PURPLE": (139,0,139,255),
        "GOLD": (255,215,0,255),
        }
BACKGROUND = CRAYONBOX["GRAY"];


# i used this one
def text_to_screen(screen, message):
    """ Displays a specified message to the game screen. 

    Parameters:
            screen - the screen that will be written to
            message - the message to be displayed

    Returns:
            None.
    """
    font = pygame.font.Font(None, 35)
    
    display = font.render(message, 1, CRAYONBOX["BLACK"])
    
    screen.blit(display, (WINDOW_WIDTH / 2 - 135,
                            WINDOW_HEIGHT / 8))


# Ideally this is the one we would use and then could pass in the positioning
# arguments as well thought the one above here is good for now.
def robust_text_to_screen(screen, font, font_size, color, message):
    """ Displays a specified message to the game screen. 

    Parameters:
            screen - the screen that will be written to
            font - the pygame font ot be used
            font_size - the size of the font 
            color - the color that will be found in the CRAYONBOX
            message - the message to be displayed

    Returns:
            None.
    """
    font = font
    display = font.render(message, 1,CRAYONBOX[color])
    screen.blit(display, (WINDOW_WIDTH / 4 - (TEXT_BOX_WIDTH),
                            WINDOW_HEIGHT / 4))


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
    input_box = pygame.Rect(WINDOW_WIDTH / 2 - (TEXT_BOX_WIDTH / 2),
                            WINDOW_HEIGHT / 4 - TEXT_BOX_HEIGHT / 2,
                            TEXT_BOX_WIDTH, TEXT_BOX_HEIGHT)

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


            # Ask the user for the number of Vertices
            message = "Enter the number of vertices: "
            text_to_screen(screen, message)
            
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

                        #pygame.draw.rect(screen, CRAYONBOX["WHITE"], input_box)
                        #txt_surface = font.render(text_input, True, text_box_color)
                        #screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

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
    display_usable_colors(screen, len(CRAYONBOX), RADIUS, THICKNESS)
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
                        recolor(screen, RADIUS, THICKNESS, pygame.key.get_pressed(), vtx["x"], vtx["y"])

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

    # Assign adjacency
    for i in range(0, number_of_vertices):
        """
        if i is not 0:
            VERTICES[i]["adjacent"].append(VERTICES[i - 1]["ID"])
        if i is not number_of_vertices - 1:
            VERTICES[i]["adjacent"].append(VERTICES[i + 1]["ID"])
        """
        if i is not number_of_vertices - 1:
            VERTICES[i]["adjacent"].append(VERTICES[i + 1]["ID"])
            VERTICES[i + 1]["adjacent"].append(VERTICES[i]["ID"])

    draw_graph(screen, VERTICES, radius, thickness)




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
        """
        if i is not 0:
            VERTICES[i]["adjacent"].append(VERTICES[i - 1]["ID"])
        else: 
            VERTICES[i]["adjacent"].append(VERTICES[number_of_vertices - 1]["ID"])

        if i is not number_of_vertices - 1:
            VERTICES[i]["adjacent"].append(VERTICES[i + 1]["ID"])
        else:
            VERTICES[i]["adjacent"].append(VERTICES[0]["ID"])
        """
        if i is not number_of_vertices - 1:
            VERTICES[i]["adjacent"].append(VERTICES[i + 1]["ID"])
            VERTICES[i + 1]["adjacent"].append(VERTICES[i]["ID"])
        else:
            VERTICES[i]["adjacent"].append(VERTICES[0]["ID"])
            VERTICES[0]["adjacent"].append(VERTICES[i]["ID"])

    draw_graph(screen, VERTICES, radius, thickness)




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
                if vtx_one is not None and vtx_two is not None and vtx_one["ID"] is not vtx_two["ID"]:
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

                # Delete the most recently made vertex and all of its adjacencies
                if event.key == pygame.K_u and vertices_created >= 1:
                    vertices_created -= 1
                    deleted = VERTICES.pop()
                    for adj in deleted["adjacent"]:
                        VERTICES[adj]["adjacent"].remove(deleted["ID"])
                    vtx_one = None
                    vtx_two = None
                    screen.fill(BACKGROUND)
                
                # Delete the most recently drawn edge
                if event.key == pygame.K_e and vertices_created >= 2:
                    if vtx_one["adjacent"] and vtx_two["adjacent"]:
                        vtx_one["adjacent"].pop()
                        vtx_two["adjacent"].pop()
                    screen.fill(BACKGROUND)



                # Close window on pressing ESC
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_c:
                    generating = False

            # If the window is closed, exit the game
            if event.type == pygame.QUIT:
                generating = False
            
            draw_graph(screen, VERTICES, RADIUS, THICKNESS)
            pygame.display.update()




def create_random_graph(screen, number_of_vertices, number_of_edges, radius, thickness):
    """
    Creates a randomly generated graph of n vertices and m edges on screen

    Generates a random x and y coordinate for each vertex. Coordinates cannot
    be within a specified distance of each other to prevent overlap.
    Assign new vertices to the vertex list.
    Pick two random vertices to connect with an edge and append them to each
    other's adjacency lists.
    Draw the graph

    Parameters:
    screen (pygame object): The game window
    number_of_vertices (int): The number of vertices to draw
    number_of_edges (int): The number of edges to draw
    radius (int): The radius of a vertex
    thickness (int): the thickness of a vertex's outer ring

    Returns:
    N/A
    """
    dist_apart = radius * 3

    for i in range(0, number_of_vertices):
        vtx_x, vtx_y = generate_valid_coordinates(radius, dist_apart)
        
        vtx = {"ID": i,
                "x": vtx_x,
                "y": vtx_y,
                "color": "WHITE",
                "adjacent": [],
                }

        VERTICES.append(vtx);

    # Assign adjacency
    for i in range(0, number_of_edges):
        vtx_one = None
        vtx_two = None

        while vtx_one is vtx_two:
            vtx_one = random.randint(0, number_of_vertices - 1)
            vtx_two = random.randint(0, number_of_vertices - 1)

        VERTICES[vtx_one]["adjacent"].append(VERTICES[vtx_two]["ID"])
        VERTICES[vtx_two]["adjacent"].append(VERTICES[vtx_one]["ID"])

    draw_graph(screen, VERTICES, RADIUS, THICKNESS)




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
    elif choice is 4:
        # Currently random - Will be user-inputted in the future
        number_of_edges = random.randint(1, 2 * number_of_vertices)
        create_random_graph(screen, number_of_vertices, number_of_edges, radius, thickness)



def draw_graph(screen, vertices, radius, thickness):
    """
    Draws a graph to the screen

    Draws a line between every pair of adjacent vertices in the vertex list.
    Draws default vertices for every vertex in the vertex list.

    Parameters:
    screen (pygame object): The game window
    vertices (list): The list of vertices for the graph
    radius (int): The radius of a vertex
    thickness (int): the thickness of a vertex's outer ring

    Returns:
    N/A
    """

    for vtx in vertices:
        for neighbor in vtx["adjacent"]:
            pygame.draw.line(screen, CRAYONBOX["BLACK"], (vtx["x"], vtx["y"]),
                    (vertices[neighbor]["x"], vertices[neighbor]["y"]), thickness)

    for vtx in vertices:
        pygame.draw.circle(screen, CRAYONBOX["BLACK"], (vtx["x"], vtx["y"]), radius, thickness)
        pygame.draw.circle(screen, CRAYONBOX["WHITE"], (vtx["x"], vtx["y"]), radius - thickness)




def generate_valid_coordinates(radius, dist_apart):
    """
    Generates a random valid coordinate pair

    Generates a random multiple of a specified distance. If that number is
    within the radius of another vertex, generate a new number. Try this
    1000 times before giving up and placing the vertex anywhere. Do this for
    both x and y coordinates

    Parameters:
    dist_apart (int): The min distance apart any two vertices can be.

    Returns:
    Two integer multiples of dist_apart that (hopefully) do not lie within
    the radius of any other vertex
    """

    vtx_x = random.randrange(dist_apart, int(WINDOW_WIDTH - radius), dist_apart);
    vtx_y = random.randrange(dist_apart, int(WINDOW_HEIGHT), dist_apart);

    count = 0
    while any((abs(vtx["x"] - vtx_x) <= dist_apart) for vtx in VERTICES) and count < 1000:
        vtx_x = random.randrange(dist_apart, int(WINDOW_WIDTH - dist_apart), dist_apart);
        count += 1

    count = 0
    while any((abs(vtx["y"] - vtx_y) <= dist_apart) for vtx in VERTICES) and count < 1000:
        vtx_y = random.randrange(dist_apart, int(WINDOW_HEIGHT), dist_apart);
        count += 1
    return vtx_x, vtx_y



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




def display_usable_colors(screen, num_colors, radius, thickness):
    """
    Displays all playable colors for the current game

    Parameters:
    screen (pygame object): The game window
    num_colors (int): The number of colors to be displayed
    radius (int): The radius of a vertex
    thickness (int): the thickness of a vertex's outer ring

    Returns:
    N/A
    """

    # The list of colors to be displayed
    colors = list(CRAYONBOX.keys())[3:num_colors]

    # How much to offset the display by
    offset = 50

    for i in range(0, len(colors)):

        x = int(i * offset + offset / 2)
        y = offset

        rad = int(radius / 2)
        thick = int(thickness / 2)

        color = colors[i]

        pygame.draw.circle(screen, CRAYONBOX[color], (x, y), rad - thick)
        pygame.draw.circle(screen, CRAYONBOX["BLACK"], (x, y), rad, thick)




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
    for vtx in VERTICES:
        vtx["color"] = CRAYONBOX["WHITE"]
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




def recolor(screen, radius, thickness, keys, vtx_x, vtx_y):
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
    elif keys[pygame.K_7]:
        new_color = "PURPLE"
    elif keys[pygame.K_8]:
        new_color = "GOLD"
    else:
        return

    if CRAYONBOX[new_color] != current_color and is_legal(vertex, new_color):
        pygame.draw.circle(screen, CRAYONBOX[new_color], (vtx_x, vtx_y), radius - thickness)
        pygame.draw.circle(screen, CRAYONBOX["BLACK"], (vtx_x, vtx_y), radius, thickness)
        vertex["color"] = new_color




if __name__ == '__main__':
    main()
