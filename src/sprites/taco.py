import pygame as pg
import random
import math as m
from src.constants import *


class Taco(pg.sprite.Sprite):
    def __init__(
        self, group: pg.sprite.Group, taco_image: pg.Surface, cheese_image: pg.Surface
    ):
        super().__init__(group)

        self.cheese_img = cheese_image
        self.taco_img = taco_image
        self.rot_img = self.taco_img.copy()

        self.side = random.choice(["left", "right"])
        if self.side == "right":
            self.taco_img = pg.transform.flip(self.taco_img, True, False)

        self.size = self.taco_img.get_size()
        start_x = (
            -self.size[0] if self.side == "left" else WIN_WIDTH + (self.size[0] / 2)
        )
        self.pos = pg.Vector2(start_x, self.size[1])
        self.rect = self.rot_img.get_frect(center=self.pos)

        self.speed = 14 if self.side == "left" else -14
        self.health = 2
        self.angle = 0

        self.cheese_group = pg.sprite.Group()
        self.old_tick = 0

        self.space = self.speed * 2
        self.hitbox = pg.FRect((self.pos.x - self.space, 0), (1, WIN_HEIGHT))

    def hit(self):
        self.health -= 1; self.kill() if self.health == 0 else None

    def throw_cheese(self):
        current_tick = pg.time.get_ticks() // 50
        if current_tick > self.old_tick and (
            -self.size[0] < self.pos.x < WIN_WIDTH + self.size[0]
        ):
            Cheese(self.cheese_group, self.cheese_img, self.pos.copy(), self.side)
            self.old_tick = current_tick

    def draw_hitbox(self):
        self.hitbox.topleft = (self.pos.x - self.space, 0)

    def update(self, dt: float):
        self.pos.x += self.speed * dt
        self.angle += dt * 100
        self.angle %= 360

        rad = m.radians(self.angle)
        pivot = m.sin(rad) * 20

        self.rot_img = pg.transform.rotate(self.taco_img, pivot)
        self.rect = self.rot_img.get_frect(center=self.pos)

        self.throw_cheese()
        for cheese in self.cheese_group:
            cheese.update(dt)
        if len(self.cheese_group) == 0:
            self.kill()

    def draw(self, screen: pg.Surface):
        screen.fblits([(cheese.rot_img, cheese.pos) for cheese in self.cheese_group])
        screen.blit(self.rot_img, self.rect)
        self.draw_hitbox()


class Cheese(pg.sprite.Sprite):
    def __init__(
        self,
        group: pg.sprite.Group,
        image: pg.Surface,
        spawn_pos: pg.Vector2,
        side: str,
    ):
        super().__init__(group)

        self.img = image
        self.rot_img = image
        self.pos = spawn_pos
        self.fall_speed = random.randint(10, 20)
        self.momentum_speed = 5
        self.side = side
        self.angle = 0

        self.turn_direction = random.choice([-1, 1])

    def update(self, dt: float) -> None:
        self.pos.y += dt * self.fall_speed
        if self.pos.y > WIN_HEIGHT:
            self.kill()
            return

        if self.side == "left":
            self.pos.x += dt * self.momentum_speed
        elif self.side == "right":
            self.pos.x -= dt * self.momentum_speed

        self.angle += dt * self.turn_direction * 20

        self.rot_img = pg.transform.rotate(self.img, self.angle)
