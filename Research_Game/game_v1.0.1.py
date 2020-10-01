##
# A small pygame program that displays a circle on a screen.
# Detects when the user has clicked within a circle
#
# Authors: Nicholas O'Kelley, Daniel Hammer, Brandon Moore
# Date: March 7th, 2020
##

"""
TODO:

    Refactor

"""

import pygame
import random
import math
import os

# Global constants
RADIUS = 35
THICCNESS = int(RADIUS / 6)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
TEXT_BOX_WIDTH = 140
TEXT_BOX_HEIGHT = 32
SYS_COLORS = 4
VERTICES = []

# Determines what you can input in the num_vertices selection box
VALID_INPUTS = (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9,
                pygame.K_ESCAPE, pygame.K_BACKSPACE, pygame.K_RETURN)

# Color dictionary, (Red,Green,Blue,Alpha)
CRAYONBOX = {
    "WHITE": (255, 255, 255, 255),
    "GRAY": (169, 169, 169, 255),
    "DARK GRAY": (128, 128, 128, 255),
    "BLACK": (0, 0, 0, 255),
    "BLUE": (0, 0, 255, 255),
    "RED": (255, 0, 0, 255),
    "GREEN": (0, 255, 0, 255),
    "YELLOW": (255, 255, 0, 255),
    "PINK": (255, 0, 255, 255),
    "CYAN": (0, 255, 255, 255),
    "PURPLE": (139, 0, 139, 255),
    "GOLD": (255, 215, 0, 255),
}

BACKGROUND = CRAYONBOX["GRAY"]
CURRENT_DIR = os.path.dirname(__file__)
GRAPH_FILES = os.path.join(CURRENT_DIR, 'prebuilt_graphs')
PREBUILT_GRAPHS = os.listdir(GRAPH_FILES)
GRAPH_TYPES = ["Custom", "Path", "Cycle", "Complete", "Prebuilt"]


def main():

    # Initialize the game
    pygame.init()
    # pygame.font.init()
    # pygame.display.init()

    # The screen variable that sets display using the width and height variables
    global screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # Sets the title bar of the screen
    pygame.display.set_caption("Competitive Graph Coloring - " + str(__file__))

    # Fills the screen with the background color
    screen.fill(BACKGROUND)

    # Create the graph
    game_over, num_colors = create_graph(RADIUS, THICCNESS)

    # The legal colors available for each game
    colors_available = list(CRAYONBOX.keys())[SYS_COLORS:num_colors]
    display_usable_colors(colors_available, RADIUS, THICCNESS)

    # Turn counter, even for player 1, odd for player 2
    turn = 0

    # Game loop
    while not game_over:

        for event in pygame.event.get():

            display_turn(turn)
            pygame.display.update()

            # Get all keys pressed
            keys = pygame.key.get_pressed()

            # Get all mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Store the click position's coordinates
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # If the circle was clicked, try to recolor it
                for vtx in VERTICES:
                    if (is_clicked(vtx["x"], vtx["y"], mouse_x, mouse_y, RADIUS)):
                        if recolor(RADIUS, THICCNESS, colors_available, keys, vtx["x"], vtx["y"]):
                            turn += 1

                        # Check to see if the game has been won
                        game_state = is_game_over(colors_available)

                        # Un-commenting this will cause the game to end
                        # and shutdown after a victory
                        # if game_state==-1 or game_state==1:
                        #    game_over = True

            if event.type == pygame.KEYDOWN:

                # Reset the game upon pressing 'r'
                if event.key == pygame.K_r:
                    reset_game(RADIUS, THICCNESS, colors_available)
                    turn = 0

                # Close window on pressing ESC
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    game_over = True

            # If the window==closed, exit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                game_over = True


def run_setup(message, menu_num):
    """
    Runs the setup window

    Displays an input box to take in the number of vertices to generate.
    Also displays a list of choices, if applicable.

    Parameters:
    message (string): The message to be displayed on screen
    menu_num (int): A flag to determine what information to show

    Returns:
    num (int): The number entered in the text box
    game_over (boolean): Whether or not the game has been stopped
    """

    global screen

    # This defines the text input box boundaries
    input_box = pygame.Rect(WINDOW_WIDTH / 2 - (TEXT_BOX_WIDTH / 2),
                            WINDOW_HEIGHT / 4 - TEXT_BOX_HEIGHT / 2,
                            TEXT_BOX_WIDTH, TEXT_BOX_HEIGHT)

    # Colors for the box on whether it==active or not
    color_inactive = CRAYONBOX["CYAN"]
    color_active = CRAYONBOX["BLUE"]

    # Default coloring of box
    text_box_color = color_inactive

    # Default font
    font = pygame.font.Font(None, 32)

    # Box and game are both active to begin with
    active = True
    game_over = False

    # Default values of the input box
    text_input = ''
    num = 1

    # Setup Window
    setup_running = True
    while setup_running:

        for event in pygame.event.get():

            # Get all mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Toggle the input box's activity
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False

                # Change the color of the input box
                text_box_color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:

                # Get all keys pressed
                keys = pygame.key.get_pressed()

                # If the text box==active and the text input==valid
                if active and event.key in VALID_INPUTS:

                    # Submit the inputted text
                    if event.key == pygame.K_RETURN:
                        if text_input == "":
                            text_input = "1"
                        num = int(text_input)
                        active = False
                        setup_running = False

                    # Decrement the text input
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]

                    # Add to text input
                    else:
                        text_input += event.unicode

                # Close window on pressing ESC
                if event.key == pygame.K_ESCAPE:
                    setup_running = False
                    game_over = True

            # If the window==closed, exit the game
            if event.type == pygame.QUIT:
                setup_running = False
                game_over = True

            # Give the text box some font
            txt_surface = font.render(text_input, True, CRAYONBOX["BLACK"])

            # Draw the input box
            input_box.w = max(TEXT_BOX_WIDTH, txt_surface.get_width() + 10)
            pygame.draw.rect(screen, text_box_color, input_box, 3)
            pygame.draw.rect(screen, CRAYONBOX["WHITE"], input_box)
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

            # Displays the message above the text box
            centered_message(message, CRAYONBOX["BLACK"], 35)

            # List all graph types for the first menu
            if menu_num==1:
                display_list("Graph types:",
                             CRAYONBOX["BLACK"], 35, GRAPH_TYPES)
            # List all available prebuilt graphs for the fourth menu
            elif menu_num==4:
                display_list("Files to choose from:",
                             CRAYONBOX["BLACK"], 35, PREBUILT_GRAPHS)

            # Update the display
            pygame.display.update()
            screen.fill(BACKGROUND)

    return num, game_over


def centered_message(message, color, font_size):
    """
    Displays a specified message to the game screen. 

    Parameters:
    message (string): The message to be displayed on screen

    Returns:
    N/A
    """

    global screen

    font = pygame.font.Font(None, font_size)

    display = font.render(message, 1, color, BACKGROUND)

    x = int((WINDOW_WIDTH / 2) - (display.get_size()[0] / 2))
    y = int(WINDOW_HEIGHT / 16)

    screen.blit(display, (x, y))


def display_turn(turn):
    """
    Displays whose turn it is

    Parameters:
    turn (int): The turn counter

    Returns:
    N/A
    """

    global screen

    font = pygame.font.Font(None, 50)

    player = turn % 2 + 1

    display = font.render("Player " + str(player) +
                          "'s turn", 1, CRAYONBOX["BLACK"], BACKGROUND)

    screen.blit(
        display, (int((WINDOW_WIDTH / 2) - (display.get_size()[0] / 2)), 10))


def display_list(message, color, font_size, items):
    """
    Displays a list of all items in 'items' to the screen

    Displays each item name with a number corresponding to its choice for the
    selection menu. Adjusts coordinates so that 10 items are listed per row.

    Parameters:
    message (string): The message to be displayed on screen
    color (tuple):The color of the text to be displayed
    font_size (int): The font size
    items (list): The items to be displayed

    Returns:
    N/A
    """

    global screen

    font = pygame.font.Font(None, font_size)

    display = font.render(message, 1, color, BACKGROUND)

    x = int((WINDOW_WIDTH / 2) - (display.get_size()[0] / 2))
    y = int(WINDOW_HEIGHT / 3)

    screen.blit(display, (x, y))
    for i in range(0, len(items)):

        # If 10 items have been listed, create a new column
        if i % 10==0:
            x = 10 + i * 31
        y = int(WINDOW_HEIGHT / 3) + ((i % 10) * 40) + 40

        display = font.render(
            str(i) + " - " + str(items[i]), 1, color, BACKGROUND)
        screen.blit(display, (x, y))


def create_path(number_of_vertices, radius, thickness):
    """
    Creates a standard path of n vertices on screen

    Creates a vertex spaced dist_apart pixels apart at the
    middle height of the screen.
    Saves each vertex as a dictionary to a vertex list
    Assigns adjacency so that each vertex has two neighbors except the
    beginning and ending vertices.

    Parameters:
    number_of_vertices (int): The number of vertices to draw
    radius (int): The radius of a vertex
    thickness (int): the thickness of a vertex's outer ring

    Returns:
    N/A
    """

    global screen

    dist_apart = radius * 3

    for i in range(0, number_of_vertices):
        vtx_x = i * dist_apart + \
            int((WINDOW_WIDTH - dist_apart * (number_of_vertices - 1)) / 2)
        vtx_y = int(WINDOW_HEIGHT / 2)

        vtx = {"ID": i,
               "x": vtx_x,
               "y": vtx_y,
               "color": "WHITE",
               "adjacent": [],
               }

        VERTICES.append(vtx)

    # Assign adjacency
    for i in range(0, number_of_vertices):
        if i != number_of_vertices - 1:
            VERTICES[i]["adjacent"].append(VERTICES[i + 1]["ID"])
            VERTICES[i + 1]["adjacent"].append(VERTICES[i]["ID"])


def create_cycle(number_of_vertices, radius, thickness):
    """
    Creates a standard cycle of n vertices on screen

    Creates a vertex spaced dist_apart pixels apart at the.
    middle height of the screen and circling around using sine/cosine values.
    Saves each vertex as a dictionary to a vertex list.
    Assigns adjacency so that each vertex has two neighbors.

    Parameters:
    number_of_vertices (int): The number of vertices to draw
    radius (int): The radius of a vertex
    thickness (int): the thickness of a vertex's outer ring

    Returns:
    N/A
    """

    global screen
    dist_apart = number_of_vertices * 15

    for i in range(0, number_of_vertices):
        vtx_x = int((WINDOW_WIDTH / 2) + math.cos((i * math.pi *
                                                   2) / number_of_vertices) * dist_apart)
        vtx_y = int((WINDOW_HEIGHT / 2) + math.sin((i * math.pi *
                                                    2) / number_of_vertices) * dist_apart)

        vtx = {"ID": i,
               "x": vtx_x,
               "y": vtx_y,
               "color": "WHITE",
               "adjacent": [],
               }

        VERTICES.append(vtx)

    # Assign adjacency
    for i in range(0, number_of_vertices):
        if i != number_of_vertices - 1:
            VERTICES[i]["adjacent"].append(VERTICES[i + 1]["ID"])
            VERTICES[i + 1]["adjacent"].append(VERTICES[i]["ID"])
        else:
            VERTICES[i]["adjacent"].append(VERTICES[0]["ID"])
            VERTICES[0]["adjacent"].append(VERTICES[i]["ID"])


def create_complete(number_of_vertices, radius, thickness):
    """
    Creates a standard complete graph of n vertices on screen

    Creates a vertex spaced dist_apart pixels apart at the.
    middle height of the screen and circling around using sine/cosine values.
    Saves each vertex as a dictionary to a vertex list.
    Assigns adjacency so that each vertex has n - 1 neighbors

    Parameters:
    number_of_vertices (int): The number of vertices to draw
    radius (int): The radius of a vertex
    thickness (int): the thickness of a vertex's outer ring

    Returns:
    N/A
    """

    global screen
    dist_apart = number_of_vertices * 15

    for i in range(0, number_of_vertices):
        vtx_x = int((WINDOW_WIDTH / 2) + math.cos((i * math.pi *
                                                   2) / number_of_vertices) * dist_apart)
        vtx_y = int((WINDOW_HEIGHT / 2) + math.sin((i * math.pi *
                                                    2) / number_of_vertices) * dist_apart)

        vtx = {"ID": i,
               "x": vtx_x,
               "y": vtx_y,
               "color": "WHITE",
               "adjacent": [],
               }

        VERTICES.append(vtx)

    # Assign adjacency
    for i in range(0, number_of_vertices):
        for j in range(i, number_of_vertices):
            if i != j:
                VERTICES[i]["adjacent"].append(VERTICES[j]["ID"])
                VERTICES[j]["adjacent"].append(VERTICES[i]["ID"])


def create_custom_graph(radius, thickness):
    """
    Generates a custom-made graph

    The users clicks while pressing 'v' or 'SPACE' to create a vertex.
    Clicking and dragging will create an edge between two vertices.
    Pressing 'c' will create the graph and begin the game.

    Parameters:
    radius (int): The radius of a vertex
    thickness (int): the thickness of a vertex's outer ring

    Returns:
    N/A
    """

    global screen
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
                if keys[pygame.K_v] or keys[pygame.K_SPACE]:
                    vtx = {"ID": vertices_created,
                           "x": mouse_x,
                           "y": mouse_y,
                           "color": "WHITE",
                           "adjacent": [],
                           }
                    VERTICES.append(vtx)
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
                if vtx_one!= None and vtx_two!= None and vtx_one["ID"]!= vtx_two["ID"]:
                    vtx_one["adjacent"].append(vtx_two["ID"])
                    vtx_two["adjacent"].append(vtx_one["ID"])

            if event.type == pygame.KEYDOWN:

                # Reset the graph generation if 'r'==pressed
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
                if event.key == pygame.K_y and vertices_created >= 2:
                    if vtx_one["adjacent"] and vtx_two["adjacent"]:
                        vtx_one["adjacent"].pop()
                        vtx_two["adjacent"].pop()
                    screen.fill(BACKGROUND)

                # Close window on pressing ESC
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_c:
                    generating = False

            # If the window==closed, exit the game
            if event.type == pygame.QUIT:
                generating = False

            draw_graph(VERTICES, RADIUS, THICCNESS)
            pygame.display.update()

    # This==for creating new graphs
    # Leave this commented out for regular play
    name = input("Please enter a name for this graph: ")
    filename = os.path.join(GRAPH_FILES, name + ".txt")
    fi = open(filename, "w")
    for vtx in VERTICES:
        fi.write(str(vtx) + "\n")
    fi.close()
    """
    """
    screen.fill(BACKGROUND)


def create_prebuilt_graph(graph_choice):
    """
    Allows users to choose from a list of prebuilt graphs

    Parameters:
    graph_choice (int): The graph chosen

    Returns:
    N/A
    """

    # Retrieves the name of the graph file
    graph_file = PREBUILT_GRAPHS[graph_choice]

    # Creates a relative path to the graph file
    filename = os.path.join(GRAPH_FILES, graph_file)

    # Reads in the content of the graph file
    vertex_list = open(filename, "r")

    for line in vertex_list:
        # Saves each line as a vertex dictionary
        vtx = eval(line)
        VERTICES.append(vtx)
    vertex_list.close()


# NOTE: This function!= used in gameplay, but used for data collection
def create_random_graph(number_of_vertices, number_of_edges, radius, thickness):
    """
    Creates a randomly generated graph of n vertices and m edges on screen

    Generates a random x and y coordinate for each vertex. Coordinates cannot
    be within a specified distance of each other to prevent overlap.
    Assign new vertices to the vertex list.
    Pick two random vertices to connect with an edge and append them to each
    other's adjacency lists.
    Draw the graph

    Parameters:
    number_of_vertices (int): The number of vertices to draw
    number_of_edges (int): The number of edges to draw
    radius (int): The radius of a vertex
    thickness (int): the thickness of a vertex's outer ring

    Returns:
    N/A
    """

    global screen

    dist_apart = radius * 3

    for i in range(0, number_of_vertices):
        vtx_x, vtx_y = generate_valid_coordinates(radius, dist_apart)

        vtx = {"ID": i,
               "x": vtx_x,
               "y": vtx_y,
               "color": "WHITE",
               "adjacent": [],
               }

        VERTICES.append(vtx)

    # Assign adjacency
    for i in range(0, number_of_edges):
        vtx_one = None
        vtx_two = None

        # Do not assign the adjacency of a vertex to itself
        while vtx_one==vtx_two:
            vtx_one = random.randint(0, number_of_vertices - 1)
            vtx_two = random.randint(0, number_of_vertices - 1)

        VERTICES[vtx_one]["adjacent"].append(VERTICES[vtx_two]["ID"])
        VERTICES[vtx_two]["adjacent"].append(VERTICES[vtx_one]["ID"])


def create_graph(radius, thickness):
    """
    Determines what graph to display based on input
    Prompts the user for type of graph, number of vertices, number of colors,
    and possible selection menus.
    Processes the number of vertices and colors.

    Parameters:
    radius (int): The radius of a vertex
    thickness (int): the thickness of a vertex's outer ring

    Returns:
    game_over (boolean): Whether or not the game has been stopped
    num_colors (int): The number of colors to be used in the game
    """

    # Default value for the number of vertices in the graph
    num_vertices = 0

    # Get the type of graph to generate
    graph_type, game_over = run_setup("Enter graph type:", 1)

    # Override invalid selections to a default value of 1
    if graph_type > 4 or graph_type < 0:
        graph_type = 1

    # If the graph!= custom or prebuilt, ask for a number of vertices
    if graph_type!= 0 and graph_type!= 4:
        num_vertices, game_over = run_setup("Enter the number of vertices", 2)

        # Minimum of 2 vertices
        if num_vertices <= 1:
            num_vertices = 2

    # Generate the graph
    if graph_type==0:
        create_custom_graph(radius, thickness)
    elif graph_type==1:
        create_path(num_vertices, radius, thickness)
    elif graph_type==2:
        create_cycle(num_vertices, radius, thickness)
    elif graph_type==3:
        create_complete(num_vertices, radius, thickness)
    elif graph_type==4:
        # Prompt the user to choose from a list of existing graphs
        graph_choice, game_over = run_setup("Choose a graph file", 4)
        create_prebuilt_graph(graph_choice)
    # elif graph_type==5:
        # Currently random - Will be user-inputted in the future
    #    number_of_edges = random.randint(1, 2 * num_vertices)
    #    create_random_graph(num_vertices, number_of_edges, radius, thickness)

    # Ask for a number of colors
    num_colors, game_over = run_setup("Enter the maximum number of colors to be used (max "
                                      + str(len(CRAYONBOX) - SYS_COLORS) + ")", 3)

    # Override invalid selections to a default value of 1
    if num_colors <= 1:
        num_colors = 2
    num_colors += SYS_COLORS

    draw_graph(VERTICES, radius, thickness)

    return game_over, num_colors


def draw_graph(vertices, radius, thickness):
    """
    Draws a graph to the screen

    Draws shadows of each vertex.
    Draws a line between every pair of adjacent vertices in the vertex list.
    Draws default vertices for every vertex in the vertex list.

    Parameters:
    vertices (list): The list of vertices for the graph
    radius (int): The radius of a vertex
    thickness (int): the thickness of a vertex's outer ring

    Returns:
    N/A
    """

    global screen

    # Draws shadows
    for vtx in vertices:
        pygame.draw.circle(
            screen, CRAYONBOX["DARK GRAY"], (vtx["x"] + 4, vtx["y"] + 4), radius)

    # Draws the edges
    for vtx in vertices:
        for adj in vtx["adjacent"]:
            draw_line(vtx["x"], vtx["y"], vertices[adj]
                      ["x"], vertices[adj]["y"], thickness)

    # Draws the vertices
    for vtx in vertices:
        draw_circle("WHITE", vtx["x"], vtx["y"], radius, thickness, vtx["ID"])


def draw_circle(color, x, y, radius, thickness, id):
    """
    Draws a circle on the screen

    Draws an outer black edge and an inner colored circle. Labels each circle.

    Parameters:
    color (string): The color to be drawn in the circle
    x (int): The x coordinate to center the circle over
    y (int): The y coordinate to center the circle over
    radius (int): The radius of a vertex
    thickness (int): the thickness of a vertex's outer ring
    id (int): The ID of the vertex to be used as a label

    Returns:
    N/A
    """

    global screen

    font_size = 30

    font = pygame.font.Font(None, font_size)

    pygame.draw.circle(screen, CRAYONBOX["BLACK"], (x, y), radius, thickness)
    pygame.draw.circle(screen, CRAYONBOX[color], (x, y), radius - thickness)

    if id!= "":
        display = font.render(str(id), 1, CRAYONBOX["BLACK"], color)
        screen.blit(display, (x - (font_size / 4), y - (font_size / 4)))


def draw_line(x_one, y_one, x_two, y_two, thickness):
    """
    Draws a line on the screen with a small shadow

    Parameters:
    x_one (int): The x coordinate to begin the line
    y_one (int): The y coordinate to begin the line
    x_two (int): The x coordinate to end the line
    y_two (int): The y coordinate to end the line
    thickness (int): the thickness of the line

    Returns:
    N/A
    """
    global screen

    pygame.draw.line(screen, CRAYONBOX["DARK GRAY"],
                     (x_one + 3, y_one + 3), (x_two + 3, y_two + 3), thickness)
    pygame.draw.line(screen, CRAYONBOX["BLACK"],
                     (x_one, y_one), (x_two, y_two), thickness)


def generate_valid_coordinates(radius, dist_apart):
    """
    Generates a random valid coordinate pair

    Generates a random multiple of a specified distance. If that number is
    within the radius of another vertex, generate a new number. Try this
    1000 times before giving up and placing the vertex anywhere. Do this for
    both x and y coordinates

    Parameters:
    radius (int): The radius of a vertex
    dist_apart (int): The min distance apart any two vertices can be.

    Returns:
    vtx_x, vtx_y (int): Two integer multiples of dist_apart that (hopefully) do not lie within
    the radius of any other vertex
    """

    vtx_x = random.randrange(dist_apart, int(
        WINDOW_WIDTH - radius), dist_apart)
    vtx_y = random.randrange(dist_apart, int(WINDOW_HEIGHT), dist_apart)

    count = 0
    while any((abs(vtx["x"] - vtx_x) <= dist_apart) for vtx in VERTICES) and count < 1000:
        vtx_x = random.randrange(dist_apart, int(
            WINDOW_WIDTH - dist_apart), dist_apart)
        count += 1

    count = 0
    while any((abs(vtx["y"] - vtx_y) <= dist_apart) for vtx in VERTICES) and count < 1000:
        vtx_y = random.randrange(dist_apart, int(WINDOW_HEIGHT), dist_apart)
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


def display_usable_colors(colors, radius, thickness):
    """
    Displays all playable colors for the current game

    Parameters:
    num_colors (int): The number of colors to be displayed
    radius (int): The radius of a vertex
    thickness (int): the thickness of a vertex's outer ring

    Returns:
    N/A
    """

    global screen

    # How much to offset the display by
    offset = 50

    for i in range(0, len(colors)):

        x = int(i * offset + offset / 2)
        y = offset

        rad = int(radius / 2)
        thick = int(thickness / 2)

        draw_circle(colors[i], x, y, rad, thick, "")


def reset_game(radius, thickness, colors_available):
    """
    Resets the game

    Recolors all vertices on screen to white and redraws every vertex.

    Parameters:
    radius (int): The radius of each vertex
    thickness (int): The thickness of a vertex's outer ring

    Returns:
    N/A
    """

    global screen

    for vtx in VERTICES:
        vtx["color"] = "WHITE"
    screen.fill(BACKGROUND)
    draw_graph(VERTICES, radius, thickness)
    display_usable_colors(colors_available, radius, thickness)


def is_legal(vtx, color):
    """
    Checks if a coloring==legal

    Loops through the vertex's neighbors and compares their colors to the
    proposed new color. If any of the neighbors are already colored with the
    proposed new color, a coloring cannot be completed.

    Parameters:
    vtx (dictionary): The vertex attempting to be colored
    color (string): The proposed new color

    Returns:
    True if no neighbors are already colored with the proposed new color
    False if any neighbor==already colored with the proposed new color
    """
    for neighbor in vtx["adjacent"]:
        if VERTICES[neighbor]["color"]==color:
            return False
    return True


def recolor(radius, thickness, colors, keys, vtx_x, vtx_y):
    """
    Recolors a vertex

    Gets the current color of the vertex.
    Sets the new color according to what key was pressed.
    If the new color!= the old color and==a legal coloring, recolor
    the vertex with the new color.


    Parameters:
    radius (int): Radius of a vertex in pixels
    thickness (int): The thickness of a vertex's outer ring
    colors (list): All legal colors in the game
    keys (boolean array): List of the state of all keyboard keys
    vtx_x (int): The vertex's center's x coordinate
    vtx_y (int): The vertex's center's y coordinate

    Returns:
    True if the vertex was successfully recolored
    False if the vertex was not recolored
    """

    global screen

    # The index of "pygame.K_1" in keys
    min_color = 49

    # Get the current color and vertex clicked on
    current_color = screen.get_at((vtx_x, vtx_y))
    vertex = {}
    for vtx in VERTICES:
        if vtx["x"] == vtx_x and vtx["y"] == vtx_y:
            vertex = vtx

    # Set the new color if possible
    try:
        new_color = colors[keys.index(1) - min_color]

    except IndexError:
        try:
            print("ERROR: " + list(CRAYONBOX.keys())[SYS_COLORS:][keys.index(1) - min_color]
                  + "!= valid in this game!")
        except IndexError:
            return

        return

    except ValueError:
        print("ERROR: You must select a color using 1-" +
              str(len(colors)) + " first!")
        return

    if CRAYONBOX[new_color] != current_color and is_legal(vertex, new_color):
        draw_circle(new_color, vtx_x, vtx_y, radius, thickness, vertex["ID"])
        vertex["color"] = new_color
        return True
    else:
        return False


def is_game_over(colors_available):
    """
    Determines if the game==over

    If every vertex==colored, player one wins and the game ends.
    If every uncolored vertex has no legal colors available, player two wins
    and the game ends.

    Parameters:
    colors_available (int): The legal colors in the game

    Returns:
    -1 if player 2 wins and a vertex cannot be colored
    1 if player 1 wins and all vertices are colored
    0 if neither case==true
    """

    num_colored = 0

    for vtx in VERTICES:
        if vtx["color"]=="WHITE":

            num_illegal_colors = 0

            # Increment the counter if the coloring!= legal
            for color in colors_available:
                if not is_legal(vtx, color):
                    num_illegal_colors += 1

            # If all colorings are illegal, return -1
            if num_illegal_colors==len(colors_available):
                print("Player 2 wins!")
                centered_message("Player 2 wins!", CRAYONBOX["WHITE"], 50)
                return -1
        else:
            num_colored += 1

    # If all vertices are colored, return 1
    if num_colored==len(VERTICES):
        print("Player 1 wins!")
        centered_message("Player 1 wins!", CRAYONBOX["WHITE"], 50)
        return 1

    return 0


if __name__ == '__main__':
    main()
