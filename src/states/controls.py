import pygame as pg
from src.constants import *
from src.button import Button


class Controls:
    def __init__(self, main):
        self.main = main

        self.last_frame = pg.Surface(WIN_SIZE)
        self.pos = pg.Vector2(WIN_WIDTH / 2 + 1, WIN_HEIGHT / 4)

        self.tint = pg.Surface(WIN_SIZE, pg.SRCALPHA)
        self.tint.fill((0, 0, 0, 160))

        self.window = main.tex.window_img
        self.window_rect = self.window.get_frect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

        self.controls_title = Button(self.pos, "CONTROLS", main.font)
        self.movement = Button(self.pos + pg.Vector2(0, 30), "WASD to move", main.font, 0.5)
        self.jump = Button(self.pos + pg.Vector2(0, 40), "SPACE to jump", main.font, 0.5)
        self.attack = Button(self.pos + pg.Vector2(0, 50), "LMB to attack", main.font, 0.5)
        self.pause = Button(self.pos + pg.Vector2(0, 60), "ESC to pause", main.font, 0.5)
        self.dash = Button(self.pos + pg.Vector2(0, 70), "LSHIFT to dash", main.font, 0.5)

        self.back_button = Button(
            pg.Vector2(self.pos.x + WIN_WIDTH / 4, WIN_HEIGHT - self.pos.y),
            "BACK",
            main.font,
            0.5,
        )

    def user_input(self) -> str:
        for ev in self.main.events:
            if ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1:
                if self.back_button.check_collision(ev.pos):
                    return "title"
            if ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE:
                return "title"

    def update(self):
        self.main.screen.blit(self.last_frame, (0, 0))
        self.main.screen.blit(self.tint, (0, 0))
        self.main.screen.blit(self.window, self.window_rect)

        self.controls_title.draw(self.main.screen)
        self.movement.draw(self.main.screen)
        self.jump.draw(self.main.screen)
        self.attack.draw(self.main.screen)
        self.pause.draw(self.main.screen)
        self.dash.draw(self.main.screen)
        self.back_button.draw(self.main.screen)
