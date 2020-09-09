"""
Author: Danny Hammer
Date: 2/13/2020
"""
import pygame as pg
import random

(win_width, win_height) = (1280, 720)
(vtx_width, vtx_height) = (50, 50)
white = (255, 255, 255)
grey = (220, 220, 220)
black = (0, 0, 0)
NUM_VERTICES = 4


# Vertex class for a sprite
class Vertex(pg.sprite.Sprite):
    def __init__(self, color, width, height):
        pg.sprite.Sprite.__init__(self)

        # Creates a sprite's image
        self.image = pg.Surface([vtx_width, vtx_height])
        self.image.fill(white)
        self.image.set_colorkey(white)

        pg.draw.circle(self.image, black, (vtx_width, vtx_height), 100)

        self.rect = self.image.get_rect()


def main():
    
    # Initialization
    pg.init()

    # Images
    logo = pg.image.load("Petersen.png")
    vtx_img = pg.image.load("vertex.png")
    pg.display.set_icon(logo)
    pg.display.set_caption("base game")

    # Create a screen
    screen = pg.display.set_mode((win_width, win_height))
    screen.fill(grey)

    # Update the entire screen
    pg.display.flip()

    # Controls game loop
    running = True

    # Sprites
    all_sprites = pg.sprite.Group()
    for i in range(NUM_VERTICES):
        vtx = Vertex(white, vtx_width, vtx_height)
        vtx.rect.x = i*100
        vtx.rect.y = i*100
        all_sprites.add(vtx)

    while running:

        # Event handling
        for event in pg.event.get():

            # Quit if the window's 'x' is pressed
            if event.type == pg.QUIT:
                running = False

            # Handles keyboard input
            elif event.type == pg.KEYDOWN:

                # Quits if 'escape' is pressed
                if event.key == pg.K_ESCAPE:
                    running = False

            # Handles mouse input
            elif event.type == pg.MOUSEBUTTONUP:

                # Retrieves the position of the cursor upon click
                pos = pg.mouse.get_pos()
                print(str(pos))
                
                # Adds a sprite to the clicked_sprites list if it was clicked on
                clicked_sprites = [s for s in all_sprites if s.rect.collidepoint(pos)]

                # Changes the color of a sprite randomly if it was clicked on
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                for s in clicked_sprites:
                    s.image.fill(color)
        
        all_sprites.draw(screen)
        pg.display.update()


if __name__ == "__main__":
    main()
