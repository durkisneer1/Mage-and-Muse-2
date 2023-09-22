import pygame as pg
import math
from src.constants import *
from src.utils import import_image


class Skull(pg.sprite.Sprite):
    def __init__(
        self,
        group: pg.sprite.Group | None,
        image: pg.Surface,
        eye_frames: list[pg.Surface],
        amplitude: float,
        eye_offset: int,
        last_stage: bool = False,
    ):
        super().__init__(group) if group else super().__init__()

        self.img = image
        self.x_offset, self.y_offset = (
            WIN_WIDTH / 2,
            WIN_HEIGHT / 2 - 17,
        )
        self.pos = pg.Vector3(self.x_offset, self.y_offset, 0)
        self.rect = self.img.get_frect(center=self.pos.xy)

        self.eye_offset = eye_offset
        self.eye_frames = eye_frames
        self.eye_pos = (
            pg.Vector2(
                self.x_offset - self.img.get_width() / 4, self.img.get_height() + 15
            ),
            pg.Vector2(
                self.x_offset + self.img.get_width() / 4, self.img.get_height() + 15
            ),
        )
        self.current_frame = 0
        self.current_flower = self.eye_frames[int(self.current_frame)]
        self.max_frames = len(self.eye_frames)

        self.angle = 0
        self.speed = 12
        self.amplitude = amplitude

        self.heart = Heart()
        self.show_heart = True if last_stage else False

    def hit(self):
        pass

    def pulse_heart(self, dt):
        self.heart.update(dt, self.pos.xy)

    def animate(self, dt: float):
        self.current_frame %= self.max_frames
        self.current_flower = self.eye_frames[int(self.current_frame)]
        self.current_frame += dt

    def update(self, dt: float):
        self.animate(dt)

        # Skull position
        rad = math.radians(self.angle)
        self.pos.y = (math.sin(rad) * self.amplitude) + self.y_offset
        self.rect.center = self.pos.xy
        self.angle += self.speed * dt
        self.angle %= 360

        # Eye positions
        y_offset = self.pos.y - self.eye_offset
        for pos in self.eye_pos:
            pos.y = y_offset

        if self.show_heart:
            self.pulse_heart(dt)

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.rect)
        for pos in self.eye_pos:
            flower_rect = self.current_flower.get_frect(center=pos)
            screen.blit(self.current_flower, flower_rect)

        if self.show_heart:
            self.heart.draw(screen)


class Heart(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.img_states = {
            "idle": import_image("./res/skull/heart.png"),
            "hit": import_image("./res/skull/heart.png", highlight=True),
        }
        self.img = self.img_states["idle"]
        self.scaled_img = self.img
        self.pos = pg.Vector3(0, 0, 1)
        self.rect = self.scaled_img.get_frect()
        self.degrees = 0
        self.offset = pg.Vector2(0, -27)

        self.SPEED = 35
        self.health = 50  # Default 150
        self.hit_time = 0

    def hit(self):
        self.health -= 1
        self.hit_time = pg.time.get_ticks()
        self.img = self.img_states["hit"]

    @staticmethod
    def square_wave(phase):
        if phase > 0.2:
            return phase + 1.5
        else:
            return 1

    def animate(self, dt: float):
        if pg.time.get_ticks() - self.hit_time > 80:
            self.img = self.img_states["idle"]

        self.degrees += dt * self.SPEED
        self.degrees %= 360
        scalar = (
            self.square_wave(
                (math.sin(math.radians(self.degrees) * 2) / 2)
                + (math.sin(math.radians(self.degrees) * 1.5) / 2)
            )
        )
        self.scaled_img = pg.transform.scale_by(self.img, scalar)

    def update(self, dt: float, pos: pg.Vector2):
        self.animate(dt)

        adj_pos = pos + self.offset
        self.rect = self.scaled_img.get_frect(center=adj_pos)

    def draw(self, screen: pg.Surface):
        screen.blit(self.scaled_img, self.rect)
