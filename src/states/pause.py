import pygame as pg
from src.constants import *
from src.button import Button
from src.enums import States


class Pause:
    def __init__(self, main):
        self.main = main

        self.last_frame = pg.Surface(WIN_SIZE)
        self.pos = pg.Vector2(WIN_WIDTH / 2 + 1, WIN_HEIGHT / 4)

        self.tint = pg.Surface(WIN_SIZE, pg.SRCALPHA)
        self.tint.fill((0, 0, 0, 160))

        self.window = main.tex.window_img
        self.window_rect = self.window.get_frect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

        self.pause_title = Button(self.pos, "PAUSED", main.font)
        self.menu_button = Button(self.pos + pg.Vector2(0, 40), "Menu", main.font)
        self.resume_button = Button(self.pos + pg.Vector2(0, 60), "Resume", main.font)

    def user_input(self, event) -> States | None:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT:
            if self.menu_button.check_collision(event.pos):
                return States.TITLE
            elif self.resume_button.check_collision(event.pos):
                return States.GAMEPLAY

        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            return States.GAMEPLAY

        return None

    def update(self):
        self.main.screen.blit(self.last_frame, (0, 0))
        self.main.screen.blit(self.tint, (0, 0))
        self.main.screen.blit(self.window, self.window_rect)

        self.pause_title.draw(self.main.screen)
        self.menu_button.draw(self.main.screen)
        self.resume_button.draw(self.main.screen)
