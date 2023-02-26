import pygame as pg
from constants import WIN_WIDTH, WIN_HEIGHT
from support import import_folder


class Background:
    def __init__(self):
        self.moving_bg_list = (
            pg.image.load("../res/desert/SandBG.png").convert_alpha(),
            pg.image.load("../res/desert/SandFG.png").convert_alpha(),
            pg.image.load("../res/desert/Clouds.png").convert_alpha(),
        )
        self.sky_anim_list = import_folder("../res/desert/sky", False)
        self.sky_img = self.sky_anim_list[0]
        self.current_frame = 0

        self.pos = pg.Vector2(0, 0)
        self.speed = 10

    def animate_sky(self, dt):
        self.current_frame += dt / 2
        if self.current_frame > len(self.sky_anim_list):
            self.current_frame = 0
        self.sky_img = self.sky_anim_list[int(self.current_frame)]

    def movement(self, dt):
        self.pos.x -= self.speed * dt

    def draw_wrapped(self, screen: pg.Surface, img_pick: int, slowdown_factor=1):
        pos_x = (self.pos.x / slowdown_factor) % WIN_WIDTH
        for i in range(-2, 3):
            screen.blit(
                self.moving_bg_list[img_pick], ((pos_x + WIN_WIDTH * i), self.pos.y)
            )

    def draw_sky(self, screen: pg.Surface):
        screen.blit(self.sky_img, (0, 0))
        pg.draw.circle(screen, (251, 242, 54), (WIN_WIDTH, WIN_HEIGHT / 2), 15)  # Sun


class Train:
    def __init__(self):
        self.img = pg.image.load("../res/train/Train.png").convert_alpha()
        self.img_width = self.img.get_width()

        self.pos = pg.Vector2(0, WIN_HEIGHT - self.img.get_height())
        self.speed = 3
        self.bounce_tick = 0

    def movement(self, dt):
        self.pos.x += self.speed * dt
        self.bounce_tick += dt * 1.5
        if self.bounce_tick > 1:
            self.speed *= -1
            self.bounce_tick = 0

    def draw(self, screen: pg.Surface):
        pos_x = self.pos.x % self.img_width
        for i in range(-2, 3):
            screen.blit(self.img, ((pos_x + self.img_width * i), self.pos.y))
