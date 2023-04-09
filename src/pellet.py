import pygame as pg
import random
from src.constants import *


class Pellet(pg.sprite.Sprite):
    def __init__(
        self,
        groups: pg.sprite.Group,
        spawn_pos: tuple,
        img: pg.Surface,
        dest: tuple[int, int] | float,
        turn_speed: int = 1,
        name: str = "pellet",
        move_method: str = "linear",
    ):
        super().__init__(groups)

        self.name = name
        self.speed = 20
        self.gravity = 3

        self.pos = pg.Vector2(
            spawn_pos[0] - img.get_width() / 2,
            (spawn_pos[1] + 5) - img.get_height() / 2,
        )
        self.img = img
        self.rect = pg.FRect(self.img.get_rect(topleft=self.pos))

        if move_method == "linear":
            self.vel = self.linear_direction(dest)
        elif move_method == "parabolic":
            self.vel = self.parabolic_direction(dest)

        self.turn_tick = 0
        self.turn_speed = turn_speed

    def rotate(self, dt: float):
        self.turn_tick += dt * self.turn_speed
        if self.turn_tick > 1:
            self.img = pg.transform.rotate(self.img, 90)
            self.turn_tick = 0

    def parabolic_direction(self, distance: float) -> pg.Vector2:
        dx = (distance / WIN_WIDTH) - 0.5
        dy = -1
        dir_vec = pg.Vector2(dx, dy) * self.speed
        return dir_vec

    def linear_direction(self, dest: tuple[int, int]) -> pg.Vector2:
        dx, dy = (dest[0] - self.pos.x, dest[1] - self.pos.y)
        unit_vec = pg.Vector2(dx, dy).normalize() * self.speed
        return unit_vec

    def parabolic_update(self, dt: float):
        self.rotate(dt)

        self.vel.y += self.gravity * dt
        self.pos += self.vel * dt
        self.rect.topleft = self.pos

        if self.pos.y > WIN_HEIGHT - 27:
            self.kill()
            return True

    def linear_update(self, dt: float):
        self.rotate(dt)

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
        spawn_pos: pg.Vector2,
        anim_frames: list[pg.Surface],
    ):
        super().__init__(groups)
        other.kill()

        self.anim_frames = anim_frames
        self.max_frames = len(self.anim_frames)
        self.img = self.anim_frames[0]

        offset_pos = (random.randint(-4, 4), random.randint(-4, 4))
        new_spawn = (spawn_pos.x + offset_pos[0], spawn_pos.y + offset_pos[1])
        self.pos = pg.Vector2(new_spawn)

        self.current_frame = 0

    def update(self, dt: float) -> None:
        self.current_frame += dt * 2
        if self.current_frame >= self.max_frames:
            self.kill()
            return
        self.img = self.anim_frames[int(self.current_frame)]

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.pos)
