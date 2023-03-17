import pygame as pg
from src.enums import Images
from src.constants import *


class Pause:
    def __init__(self, last_frame):
        self.last_frame = last_frame
        self.tint = pg.Surface(WIN_SIZE, pg.SRCALPHA)
        self.tint.fill((0, 0, 0, 160))
        self.window = pg.image.load(Images.pause_window.value).convert()
        self.window_rect = self.window.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

    def user_input(
        self,
        mouse_click: tuple[bool, bool, bool],
        mouse_pos: tuple[int, int],
        *args,
    ):
        ...

    def update(self, screen, *args):
        screen.blit(self.last_frame, (0, 0))
        screen.blit(self.tint, (0, 0))
        screen.blit(self.window, self.window_rect)
