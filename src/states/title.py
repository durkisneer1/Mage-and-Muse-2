import pygame as pg
from src.constants import *
from src.button import Button


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

    def user_input(self) -> str:
        for ev in self.main.events:
            if ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1:
                if self.start_button.check_collision(ev.pos):
                    return "gameplay"
                elif self.controls_button.check_collision(ev.pos):
                    return "controls"
                elif self.exit_button.check_collision(ev.pos):
                    return "exit"

    def update(self):
        self.main.screen.blit(self.bg_img, (0, 0))
        self.start_button.draw(self.main.screen)
        self.controls_button.draw(self.main.screen)
        self.exit_button.draw(self.main.screen)
