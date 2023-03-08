import pygame as pg
import random
import math as m
from constants import *


class Taco(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, img: pg.Surface):
        super().__init__(group)

        self.img = img
        self.rot_img = self.img.copy()
        self.side = random.choice(["left", "right"])
        if self.side == "right":
            self.img = pg.transform.flip(self.img, True, False)

        self.size = self.img.get_size()
        start_x = (
            -self.size[0] if self.side == "left" else WIN_WIDTH + (self.size[0] / 2)
        )
        self.pos = pg.Vector2(start_x, self.size[1])
        self.rect = self.rot_img.get_rect(center=self.pos)

        self.speed = 14 if self.side == "left" else -14
        self.health = 2
        self.angle = 0

        self.cheese_group = pg.sprite.Group()
        self.old_tick = 0

        self.space = self.speed * 2
        self.hitbox = pg.Rect((self.pos.x - self.space, 0), (1, WIN_HEIGHT))

    def hit(self):
        self.health -= 1
        if self.health == 0:
            self.kill()

    def throw_cheese(self):
        current_tick = pg.time.get_ticks() // 50
        if current_tick > self.old_tick:
            Cheese(self.cheese_group, self.pos.copy(), self.side)
            self.old_tick = current_tick

    def draw_hitbox(self):
        self.hitbox.topleft = (self.pos.x - self.space, 0)

    def update(self, dt: float) -> bool:
        self.pos.x += self.speed * dt
        self.angle += dt * 100
        self.angle %= 360

        rad = m.radians(self.angle)
        pivot = m.sin(rad) * 20

        self.rot_img = pg.transform.rotate(self.img, pivot)
        self.rect = self.rot_img.get_rect(center=self.pos)

        self.throw_cheese()
        for cheese in self.cheese_group:
            cheese.update(dt)

        return (
            self.rect.right < -self.size[0] or self.rect.left > WIN_WIDTH + self.size[1]
        )

    def draw(self, screen: pg.Surface):
        for cheese in self.cheese_group:
            cheese.draw(screen)
        screen.blit(self.rot_img, self.rect)
        self.draw_hitbox()


class Cheese(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, spawn_pos: pg.Vector2, side: str):
        super().__init__(group)

        self.img = pg.image.load("../res/taco/cheese.png").convert()

        self.pos = spawn_pos
        self.speed = random.randint(10, 20)
        self.side = side
        self.angle = 0

        self.turn_direction = random.choice([-1, 1])

    def update(self, dt: float):
        self.pos.y += dt * self.speed
        if self.side == "left":
            self.pos.x += dt * 5
        elif self.side == "right":
            self.pos.x -= dt * 5

        self.angle += dt * self.turn_direction * 20

    def draw(self, screen: pg.Surface):
        rot_img = pg.transform.rotate(self.img, self.angle)
        screen.blit(rot_img, self.pos)
