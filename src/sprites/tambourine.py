import pygame as pg
from random import choice
from src.constants import WIN_WIDTH


class Tambourine(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, image: pg.Surface):
        super().__init__(group)

        self.left = choice([True, False])
        self.rot_direction = -1 if self.left else 1
        self.pos = pg.Vector2(0 if self.left else WIN_WIDTH, 0)
        
        self.velocity = 10
        # speed by which the velocity decreases
        self.velocity_speed = 0.15
        # point at which velocity is too small
        self.velocity_limit = 5

        self.image = image
        self.rot_image = image.copy()
        self.rect = self.image.get_frect(center=self.pos)
        self.hitbox = self.rect.inflate(-8, -8)
        self.angle = 0
        self.health = 2

    def hit(self):
        self.health -= 1
        if self.health == 0:
            self.kill()

    def rotate(self, dt: float):
        self.angle += dt * 50 * self.rot_direction
        self.angle %= 360
        self.rot_image = pg.transform.rotate(self.image, self.angle)

    def update(self, dt: float, player_pos: pg.Vector2):
        self.rotate(dt)

        self.rect = self.rot_image.get_frect(center=self.pos)
        
        # decrease the velocity
        self.velocity -= self.velocity_speed * dt
        # when the velocity becomes too small
        if self.velocity <= self.velocity_limit:
            self.kill()
        # move the tambourine to the player
        self.pos.move_towards_ip(player_pos, self.velocity * dt)
        
        self.hitbox.center = self.rect.center = self.pos

    def draw(self, screen: pg.Surface):
        screen.blit(self.rot_image, self.rect)
