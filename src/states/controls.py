import pygame as pg
from src.enums import Images
from src.constants import *
from src.button import Button


class Controls:
    def __init__(self, font: pg.font.Font):
        self.last_frame = pg.Surface(WIN_SIZE)
        self.pos = pg.Vector2(WIN_WIDTH / 2 + 1, WIN_HEIGHT / 4)

        self.tint = pg.Surface(WIN_SIZE, pg.SRCALPHA)
        self.tint.fill((0, 0, 0, 160))

        self.window = pg.image.load(Images.window_img).convert()
        self.window_rect = self.window.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))

        self.controls_title = Button(self.pos, "CONTROLS", font)
        self.movement = Button(self.pos + pg.Vector2(0, 30), "WASD to move", font, 0.5)
        self.jump = Button(self.pos + pg.Vector2(0, 40), "SPACE to jump", font, 0.5)
        self.attack = Button(
            self.pos + pg.Vector2(0, 50), "LMB to attack", font, 0.5
        )
        self.pause = Button(self.pos + pg.Vector2(0, 60), "ESC to pause", font, 0.5)
        self.dash = Button(self.pos + pg.Vector2(0, 70), "LSHIFT to dash", font, 0.5)

        self.back_button = Button(
            pg.Vector2(self.pos.x + WIN_WIDTH / 4, WIN_HEIGHT - self.pos.y),
            "BACK",
            font,
            0.5,
        )

    def user_input(
        self,
        events: list[pg.event.Event],
        *args,
    ):
        for ev in events:
            if ev.type == pg.MOUSEBUTTONDOWN and ev.button == 1:
                if self.back_button.check_collision(ev.pos):
                    return "title"
            if ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE:
                return "title"

    def update(self, screen: pg.Surface, *args):
        screen.blit(self.last_frame, (0, 0))
        screen.blit(self.tint, (0, 0))
        screen.blit(self.window, self.window_rect)

        self.controls_title.draw(screen)
        self.movement.draw(screen)
        self.jump.draw(screen)
        self.attack.draw(screen)
        self.pause.draw(screen)
        self.dash.draw(screen)
        self.back_button.draw(screen)
