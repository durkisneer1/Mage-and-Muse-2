import pygame as pg
import math as m
from src.constants import *
from src.support import import_folder


class Skull(pg.sprite.Sprite):
    def __init__(
        self,
        group: pg.sprite.Group | None,
        image_dir: str,
        eye_dir: list[pg.Surface],
        amplitude: float,
        eye_offset: int,
    ):
        super().__init__(group) if group else super().__init__()

        self.img = pg.image.load(image_dir).convert_alpha()
        self.x_offset, self.y_offset = (
            WIN_WIDTH / 2,
            WIN_HEIGHT / 2 - 17,
        )
        self.pos = pg.Vector3(self.x_offset, self.y_offset, 0)
        self.rect = pg.FRect(self.img.get_rect(center=self.pos.xy))

        self.eye_offset = eye_offset
        self.eye_frames = eye_dir
        self.eye_pos = [
            pg.Vector2(
                self.x_offset - self.img.get_width() / 4, self.img.get_height() + 15
            ),
            pg.Vector2(
                self.x_offset + self.img.get_width() / 4, self.img.get_height() + 15
            ),
        ]
        self.current_frame = 0
        self.current_flower = self.eye_frames[int(self.current_frame)]
        self.max_frames = len(self.eye_frames)

        self.angle = 0
        self.speed = 12
        self.amplitude = amplitude

    def hit(self):
        ...

    def animate(self, dt):
        self.current_frame %= self.max_frames
        self.current_flower = self.eye_frames[int(self.current_frame)]
        self.current_frame += dt

    def update(self, dt: float):
        self.animate(dt)

        rad = m.radians(self.angle)
        self.pos.y = (m.sin(rad) * self.amplitude) + self.y_offset
        self.rect.center = self.pos.xy
        self.angle += self.speed * dt
        self.angle %= 360

        for pos in self.eye_pos:
            pos.y = self.pos.y - self.eye_offset

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.rect)
        for pos in self.eye_pos:
            flower_rect = self.current_flower.get_rect(center=pos)
            screen.blit(self.current_flower, flower_rect)
