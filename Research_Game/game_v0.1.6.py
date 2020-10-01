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
# 1- path
# 2- cycle
# 3- custom
# 4- random
# 5- complete
TYPE_OF_GRAPH = 4

# Determines what you can input in the num_vertices selection box
VALID_INPUTS = (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9,
                pygame.K_ESCAPE, pygame.K_BACKSPACE, pygame.K_RETURN)

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
COLOR_INACTIVE = CRAYONBOX["CYAN"]
COLOR_ACTIVE = CRAYONBOX["BLUE"]




def main():
    pygame.init()
    pygame.font.init()
    
    # The screen variable that sets display using the width and height variables
    global screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # Sets the title bar of the screen
    pygame.display.set_caption(__file__)

    # Fills the screen with the color
    screen.fill(BACKGROUND)


    #define a quick font
    font = pygame.font.Font(None, 32)


    num_vertices = 0
    num_vertices, game_over = run_setup(font, "Enter the number of vertices")
    num_colors, game_over = run_setup(font, "Enter the maximum number of colors to be used (max " + str(len(list(CRAYONBOX.keys())[3:])) + ")")
    num_colors += 3
    colors_available = list(CRAYONBOX.keys())[3:num_colors]

    # Create a graph
    create_graph(num_vertices, RADIUS, THICKNESS, TYPE_OF_GRAPH)
    display_usable_colors(num_colors, RADIUS, THICKNESS)





    # Game loop
    while not game_over:

        for event in pygame.event.get():

            pygame.display.update()

            # Get all keys pressed
            keys = pygame.key.get_pressed()
            # Get all mouse click events
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Store the click position's coordinates
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # If the circle was clicked, recolor it
                for vtx in VERTICES:
                    if (is_clicked(vtx["x"], vtx["y"], mouse_x, mouse_y, RADIUS)):
                        recolor(RADIUS, THICKNESS, num_colors, keys, vtx["x"], vtx["y"])
                        print("You clicked vtx #" + str(vtx["ID"]))
                game_over = is_game_over(colors_available)

            if event.type == pygame.KEYDOWN:

                # Reset the game upon pressing 'r'
                if event.key == pygame.K_r:
                    reset_game(RADIUS, THICKNESS)

                # Close window on pressing ESC
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    game_over = True

            # If the window is closed, exit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                game_over = True
            pygame.display.update()
    pygame.time.wait(3000)









def run_setup(font, message):
    """
    Runs the setup window

    Displays an input box to take in the number of vertices to generate.


    Parameters:
    font (pygame object): The font to be displayed

    Returns:
    num (int): The number entered in the text box
    game_over (boolean): Whether or not the game has been stopped
    """

    global screen

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
    game_over = False

    #default box value is blank
    text_input = ''
    num = 1

    
    # If the graph is a custom graph, give default values and skip setup
    #setup_running = False if TYPE_OF_GRAPH is 3 else True
    setup_running = True

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

            if event.type == pygame.KEYDOWN:

                # Get all keys pressed
                keys = pygame.key.get_pressed()

                # If the text box is active and the text input is valid
                if active and event.key in VALID_INPUTS:

                    # Submit the inputted text
                    if event.key == pygame.K_RETURN:
                        if text_input == "":
                            text_input = "2"
                        num = int(text_input);
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


            # If the window is closed, exit the game
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

            # Ask the user for the number of Vertices
            text_to_screen(message, CRAYONBOX["BLACK"], 35)

            # Update the display
            pygame.display.update()
            screen.fill(BACKGROUND)

    if num is 1 or num == "":
        num = 2

    return num, game_over




def text_to_screen(message, color, size):
    """
    Displays a specified message to the game screen. 

    Parameters:
    message (string) - The message to be displayed

    Returns:
    N/A
    """
    
    global screen

    font = pygame.font.Font(None, size)
    
    display = font.render(message, 1, color)
    
    screen.blit(display, (WINDOW_WIDTH / 2 - (display.get_size()[0] / 2),
                            WINDOW_HEIGHT / 8))




def create_path(number_of_vertices, radius, thickness):
    """
    Creates a standard path of n vertices on screen

    Creates a circle to keep track of the last color played
    Creates a vertex spaced dist_apart pixels apart at the
        middle height of the screen
    Draws lines connecting each vertex
    Saves a dictionary of each vertex's center

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
        if i is not number_of_vertices - 1:
            VERTICES[i]["adjacent"].append(VERTICES[i + 1]["ID"])
            VERTICES[i + 1]["adjacent"].append(VERTICES[i]["ID"])

    draw_graph(VERTICES, radius, thickness)




def create_cycle(number_of_vertices, radius, thickness):
    """
    Creates a standard cycle of n vertices on screen

    Creates a circle to keep track of the last color played
    Creates a vertex spaced dist_apart pixels apart at the
        middle height of the screen
    Draws lines connecting each vertex
    Saves a dictionary of each vertex's center

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
        if i is not number_of_vertices - 1:
            VERTICES[i]["adjacent"].append(VERTICES[i + 1]["ID"])
            VERTICES[i + 1]["adjacent"].append(VERTICES[i]["ID"])
        else:
            VERTICES[i]["adjacent"].append(VERTICES[0]["ID"])
            VERTICES[0]["adjacent"].append(VERTICES[i]["ID"])

    draw_graph(VERTICES, radius, thickness)




def create_complete(number_of_vertices, radius, thickness):
    """
    Creates a standard complete graph of n vertices on screen

    Creates a circle to keep track of the last color played
    Creates a vertex spaced dist_apart pixels apart at the
        middle height of the screen
    Draws lines connecting each vertex
    Saves a dictionary of each vertex's center

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
        for j in range(i, number_of_vertices):
            if i is not j:
                VERTICES[i]["adjacent"].append(VERTICES[j]["ID"])
                VERTICES[j]["adjacent"].append(VERTICES[i]["ID"])

    draw_graph(VERTICES, radius, thickness)




def create_custom_graph(radius, thickness):
    """
    Generates a custom-made graph

    The users clicks while pressing 'v' to create a vertex. Clicking and
    dragging will create an edge between two vertices. Pressing 'c' will create
    the graph and begin the game.

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
            
            draw_graph(VERTICES, RADIUS, THICKNESS)
            pygame.display.update()




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

    draw_graph(VERTICES, RADIUS, THICKNESS)




def create_graph(number_of_vertices, radius, thickness, choice):
    """
    Determines what graph to display based on input

    Parameters:
    number_of_vertices (int): The number of vertices to draw
    radius (int): The radius of a vertex
    thickness (int): the thickness of a vertex's outer ring
    choice (int): The graph to generate

    Returns:
    N/A
    """

    global screen

    if choice is 1:
        create_path(number_of_vertices, radius, thickness)
    elif choice is 2:
        create_cycle(number_of_vertices, radius, thickness)
    elif choice is 3:
        create_custom_graph(radius, thickness)
    elif choice is 4:
        # Currently random - Will be user-inputted in the future
        number_of_edges = random.randint(1, 2 * number_of_vertices)
        create_random_graph(number_of_vertices, number_of_edges, radius, thickness)
    elif choice is 5:
        create_complete(number_of_vertices, radius, thickness)



def draw_graph(vertices, radius, thickness):
    """
    Draws a graph to the screen

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
    radius (int): The radius of a vertex
    dist_apart (int): The min distance apart any two vertices can be.

    Returns:
    vtx_x, vtx_y (int): Two integer multiples of dist_apart that (hopefully) do not lie within
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




def display_usable_colors(num_colors, radius, thickness):
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




def reset_game(radius, thickness):
    """
    Resets the game

    Recolors all vertices on screen to white, including the last color used slot

    Parameters:
    radius (int): The radius of each vertex
    thickness (int): the thickness of a vertex's outer ring

    Returns:
    N/A
    """

    global screen

    for vtx in VERTICES:
        vtx["color"] = "WHITE"
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




def recolor(radius, thickness, num_colors, keys, vtx_x, vtx_y):
    """
    Recolors a vertex

    Gets the current color of the vertex
    Sets the new color according to what key was pressed
    If the new color is not the old color, recolor the vertex
    

    Parameters:
    radius (int): Radius of a vertex in pixels
    keys (boolean array): List of the state of all keyboard keys
    vtx_x (int): The vertex's center's x coordinate
    vtx_y (int): The vertex's center's y coordinate

    Returns:
    N/A

    """

    global screen

    # A list of the available colors in the game
    colors = list(CRAYONBOX.keys())[3:num_colors]

    # The index of "pygame.K_1" in keys
    min_color = 49

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
            print("ERROR: " + list(CRAYONBOX.keys())[3:][keys.index(1) - min_color] + " is not valid in this game!")
        except IndexError:
            return

        return

    except ValueError:
        print("ERROR: You must select a color using 1-" + str(num_colors - 3) + " first!")
        return

    if CRAYONBOX[new_color] != current_color and is_legal(vertex, new_color):
        pygame.draw.circle(screen, CRAYONBOX[new_color], (vtx_x, vtx_y), radius - thickness)
        pygame.draw.circle(screen, CRAYONBOX["BLACK"], (vtx_x, vtx_y), radius, thickness)
        vertex["color"] = new_color




def is_game_over(colors_available):
    """
    Determines if the game is over

    If every vertex is colored, player one wins and the game ends.
    If every uncolored vertex has no legal colors available, player two wins
    and the game ends.

    Parameters:
    colors_available (int): The number of legal legal in the game

    Returns:
    True if all vertices are colored.
    True if no legal coloring exists for any vertex.
    False otherwise.
    """

    num_colored = 0

    for vtx in VERTICES:
        if vtx["color"] is not "WHITE":
            num_colored += 1

        # For every uncolored vertex
        else:
            num_illegal_colors = 0
            # Increment the counter if the coloring is not legal
            for color in colors_available:
                if not is_legal(vtx, color):
                    num_illegal_colors += 1

            # If all colorings are illegal, return true
            if num_illegal_colors is len(colors_available):
                print("Player 2 wins!")
                text_to_screen("Player 2 wins!", CRAYONBOX["WHITE"], 50)
                return True


    # If all vertices are colored, return true
    if num_colored is len(VERTICES):
        print("Player 1 wins!")
        text_to_screen("Player 1 wins!", CRAYONBOX["WHITE"], 50)
        return True



if __name__ == '__main__':
    main()
