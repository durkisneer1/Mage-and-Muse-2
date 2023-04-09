import pygame as pg
from src.constants import WIN_WIDTH, WIN_HEIGHT
from src.support import import_folder
import math as m


class Background:
    def __init__(self):
        self.moving_bg_list = (
            pg.image.load("./res/desert/SandBG.png").convert_alpha(),
            pg.image.load("./res/desert/SandFG.png").convert_alpha(),
            pg.image.load("./res/desert/Clouds.png").convert_alpha(),
        )
        self.sky_anim_list = import_folder("./res/desert/sky", False)
        self.sky_img = self.sky_anim_list[0]
        self.max_sky_frames = len(self.sky_anim_list)
        self.current_frame = 0

        self.pos = pg.Vector2(0, 0)
        self.speed = 10

    def animate(self, dt):
        self.current_frame %= self.max_sky_frames
        self.sky_img = self.sky_anim_list[int(self.current_frame)]
        self.current_frame += dt / 2

    def update(self, dt):
        self.animate(dt)
        self.pos.x -= self.speed * dt

    def draw_wrapped(self, screen: pg.Surface, img_pick: int, slowdown_factor=1):
        pos_x = (self.pos.x / slowdown_factor) % WIN_WIDTH
        for i in range(-1, 2):
            screen.blit(
                self.moving_bg_list[img_pick], ((pos_x + WIN_WIDTH * i), self.pos.y)
            )

    def draw(self, screen: pg.Surface, is_day: bool):
        screen.blit(self.sky_img, (0, 0))
        color = (251, 242, 54) if is_day else (255, 255, 255)
        pg.draw.circle(screen, color, (WIN_WIDTH, WIN_HEIGHT / 2), 15)  # Sun/Moon
        self.draw_wrapped(screen, 0, 2)
        self.draw_wrapped(screen, 1, 1)
        self.draw_wrapped(screen, 2, 4)


class Train:
    def __init__(self):
        self.img = pg.image.load("./res/train/Train.png").convert_alpha()
        self.img_width = self.img.get_width()

        self.x_offset = -8
        self.pos = pg.Vector2(self.x_offset, WIN_HEIGHT - self.img.get_height())
        self.speed = 3
        self.angle = 0

    def update(self, dt: float):
        rad = m.radians(self.angle)
        x_pos = m.sin(rad) + self.x_offset
        self.pos.x = x_pos
        self.angle += dt * 250
        self.angle %= 360

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.pos)


class TrainFire(pg.sprite.Sprite):
    def __init__(
        self,
        group: pg.sprite.Group,
        fire_frames: list[pg.Surface],
        x_offset: int,
    ):
        super().__init__(group)

        self.max_frames = len(fire_frames)
        self.frame_list = fire_frames
        self.current_frame = 0
        self.anim_speed = 1.5
        self.fire_img = self.frame_list[self.current_frame]
        fire_size = self.fire_img.get_size()

        self.pos = pg.Vector2(
            x_offset - fire_size[0] / 2, WIN_HEIGHT - fire_size[1] - 29
        )

        self.loops = 0

    def update(self, dt: float):
        if self.current_frame >= self.max_frames:
            self.current_frame = 0
            self.loops += 1
        self.fire_img = self.frame_list[int(self.current_frame)]
        self.current_frame += self.anim_speed * dt

        if self.loops > 4:
            self.kill()

    def draw(self, screen: pg.Surface):
        screen.blit(self.fire_img, self.pos)
