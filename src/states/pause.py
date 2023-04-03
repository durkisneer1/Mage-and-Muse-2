import pygame as pg
from src.enums import Images
from src.constants import *
from src.button import Button


class Pause:
    def __init__(self, font: pg.font.Font):
        self.last_frame = pg.Surface(WIN_SIZE)
        self.pos = pg.Vector2(WIN_WIDTH / 2 + 1, WIN_HEIGHT / 4)

        self.tint = pg.Surface(WIN_SIZE, pg.SRCALPHA)
        self.tint.fill((0, 0, 0, 160))

        self.window = pg.image.load(Images.window_img).convert()
        self.window_rect = self.window.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

        self.pause_title = Button(self.pos, "PAUSED", font)
        self.menu_button = Button(self.pos + pg.Vector2(0, 40), "Menu", font)
        self.resume_button = Button(self.pos + pg.Vector2(0, 60), "Resume", font)

    def user_input(
        self,
        events: list[pg.event.Event],
        *args,
    ):
        for ev in events:
            if ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1:
                if self.menu_button.check_collision(ev.pos):
                    return "title"
                elif self.resume_button.check_collision(ev.pos):
                    return "gameplay"
            if ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE:
                return "gameplay"

    def update(self, screen: pg.Surface, *args):
        screen.blit(self.last_frame, (0, 0))
        screen.blit(self.tint, (0, 0))
        screen.blit(self.window, self.window_rect)

        self.pause_title.draw(screen)
        self.menu_button.draw(screen)
        self.resume_button.draw(screen)
