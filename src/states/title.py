import pygame as pg
from src.constants import *
from src.button import Button
from src.enums import States


class Title:
    def __init__(self, main):
        self.main = main

        self.bg_img = pg.Surface(WIN_SIZE)
        self.bg_img.fill("lightgray")

        self.start_button = Button((WIN_WIDTH / 2, WIN_HEIGHT / 2), "Start", main.font)
        self.controls_button = Button(
            (WIN_WIDTH / 2, WIN_HEIGHT / 2 + 20), "Controls", main.font
        )
        self.exit_button = Button((WIN_WIDTH / 2, WIN_HEIGHT / 2 + 40), "Exit", main.font)

    def user_input(self, event) -> States | None:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT:
            if self.start_button.check_collision(event.pos):
                return States.GAMEPLAY
            elif self.controls_button.check_collision(event.pos):
                return States.CONTROLS
            elif self.exit_button.check_collision(event.pos):
                return States.EXIT

        return None

    def update(self):
        self.main.screen.blit(self.bg_img, (0, 0))
        self.start_button.draw(self.main.screen)
        self.controls_button.draw(self.main.screen)
        self.exit_button.draw(self.main.screen)
