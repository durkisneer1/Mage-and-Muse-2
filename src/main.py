import pygame as pg
from constants import *
from level import Level

pg.init()

screen = pg.display.set_mode(WIN_SIZE, pg.SCALED)
pg.display.set_caption("Mage and Muse 2")

clock = pg.time.Clock()
level = Level()


def main():
    run = True
    while run:
        dt = clock.tick() / 100

        keys = pg.key.get_pressed()
        mouse_click = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()
        events = pg.event.get()

        for ev in events:
            if ev.type == pg.QUIT:
                run = False
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    run = False

        screen.fill("black")
        level.user_input(dt, mouse_click, mouse_pos)
        level.collision()
        level.update(dt, keys, mouse_pos, events, screen)

        pg.display.flip()
        pg.display.set_caption(f"{int(clock.get_fps())} fps")


if __name__ == "__main__":
    main()
