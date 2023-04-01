import pygame as pg
from src.constants import *
from src.button import Button


class Title:
    def __init__(self, font: pg.font.Font):
        self.bg_img = pg.Surface(WIN_SIZE)
        self.bg_img.fill("lightgray")

        self.start_button = Button((WIN_WIDTH / 2, WIN_HEIGHT / 2), "Start", font)
        self.controls_button = Button(
            (WIN_WIDTH / 2, WIN_HEIGHT / 2 + 20), "Controls", font
        )
        self.exit_button = Button((WIN_WIDTH / 2, WIN_HEIGHT / 2 + 40), "Exit", font)

    def user_input(
        self,
        events: list[pg.event.Event],
        *args,
    ) -> str:
        for ev in events:
            if ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1:
                if self.start_button.check_collision(ev.pos):
                    return "gameplay"
                elif self.controls_button.check_collision(ev.pos):
                    return "controls"
                elif self.exit_button.check_collision(ev.pos):
                    return "exit"

    def update(self, screen: pg.Surface, *args):
        screen.blit(self.bg_img, (0, 0))
        self.start_button.draw(screen)
        self.controls_button.draw(screen)
        self.exit_button.draw(screen)
