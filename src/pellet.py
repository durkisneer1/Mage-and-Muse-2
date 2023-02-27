import pygame as pg
import random
from constants import *


class Pellet(pg.sprite.Sprite):
    def __init__(
        self,
        groups: pg.sprite.Group,
        spawn_pos: tuple,
        img: pg.Surface,
        mouse_pos: tuple,
    ):
        super().__init__(groups)

        self.speed = 20
        self.pos = pg.Vector2(
            spawn_pos[0] - img.get_width() / 2,
            (spawn_pos[1] + 5) - img.get_height() / 2,
        )
        self.img = img
        self.rect = self.img.get_rect(topleft=self.pos)
        self.vel = self.direction(mouse_pos)

        self.turn_tick = 0

    def rotate(self, dt: float):
        self.turn_tick += dt
        if self.turn_tick > 1:
            self.img = pg.transform.rotate(self.img, 90)
            self.turn_tick = 0

    def direction(self, mouse_pos: tuple[int, int]) -> pg.Vector2:
        xy_diff = (mouse_pos[0] - self.pos.x, mouse_pos[1] - self.pos.y)
        unit_vec = pg.Vector2(xy_diff).normalize() * self.speed
        return unit_vec

    def movement(self, dt: float):
        self.pos += self.vel * dt
        self.rect.topleft = self.pos
        if (
            self.pos.x < 0
            or self.pos.x > WIN_WIDTH
            or self.pos.y < 0
            or self.pos.y > WIN_HEIGHT
        ):
            self.kill()

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.pos)


class PelletExplode(pg.sprite.Sprite):
    def __init__(
        self,
        other: Pellet,
        groups: pg.sprite.Group,
        spawn_pos: tuple[float, float],
        anim_frames: list[pg.Surface],
    ):
        super().__init__(groups)
        other.kill()

        self.anim_frames = anim_frames
        self.max_frames = len(self.anim_frames)
        self.img = self.anim_frames[0]

        offset_pos = (random.randint(-4, 4), random.randint(-4, 4))
        new_spawn = (spawn_pos[0] + offset_pos[0], spawn_pos[1] + offset_pos[1])
        self.pos = pg.Vector2(new_spawn)

        self.current_frame = 0

    def animate(self, dt: float) -> None:
        self.current_frame += dt * 2
        if self.current_frame >= self.max_frames:
            self.kill()
            return
        self.img = self.anim_frames[int(self.current_frame)]

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.pos)
