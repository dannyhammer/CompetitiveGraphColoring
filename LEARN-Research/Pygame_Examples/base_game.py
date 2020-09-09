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

"""
vtx_circle = pg.Surface((vtx_width, vtx_height), pg.SRCALPHA)
pg.gfxdraw.aacircle(vtx_circle, 0, 0, 100, grey)
pg.gfxdraw.filled_circle(vtx_circle, 0, 0, 100, grey)
"""

class Vertex(pg.sprite.Sprite):
    def __init__(self, color, width, height):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([vtx_width, vtx_height])
        self.image.fill(white)
        #self.image.set_colorkey(white)

        pg.draw.circle(self.image, black, (int(vtx_width/2), int(vtx_height/2)), 25)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        ##self.image = vtx_circle
        ##self.rect = self.image.get_rect(center=(100, 100))
    def recolor(self, color):
        pg.draw.circle(self.image, color, (int(vtx_width/2), int(vtx_height/2)), 25)
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
    for i in range(4):
        vtx = Vertex(white, vtx_width, vtx_height)
        vtx.rect.x = i*100
        vtx.rect.y = i*100
        all_sprites.add(vtx)


    while running:

        # Event handling
        for event in pg.event.get():
            # only quit if the event is of type QUIT
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            elif event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                #x, y = ph.mouse.get_pos()
                print(str(pos))
                clicked_sprites = [s for s in all_sprites if s.rect.collidepoint(pos)]
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                for s in clicked_sprites:
                    s.recolor(color)
                    s.image.fill(color)

        #screen.blit(vtx_img, (100, 100))


        all_sprites.draw(screen)
        pg.display.update()


if __name__ == "__main__":
    main()
