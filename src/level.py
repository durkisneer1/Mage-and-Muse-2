import pygame as pg
import random
from support import import_folder
from player import Player, Wand
from maraca import Maraca
from bull import Bull
from decor import Background, Train
from pellet import Pellet, PelletExplode


class Level:
    def __init__(self):
        # Level Setup Setup
        self.player = Player()
        self.wand = Wand()
        self.background = Background()
        self.train = Train()

        # Maraca Setup
        self.maraca_group = pg.sprite.Group()
        Maraca(self.maraca_group, True)
        Maraca(self.maraca_group, False)

        # Bull Attack Setup
        self.ATTACK_EVENT = pg.event.custom_type()
        pg.time.set_timer(self.ATTACK_EVENT, 2500)
        self.bull_group = pg.sprite.Group()
        self.bull_frames = import_folder("../res/bull")

        # Pellet Setup
        self.max_delay = 2.5
        self.pellet_delay = self.max_delay
        self.hit_explosion_group = pg.sprite.Group()
        self.pellet_group = pg.sprite.Group()
        self.pellet_img = pg.image.load(
            "../res/misc/projectile/Projectile.png"
        ).convert()
        self.pellet_frames = import_folder("../res/misc/projectile/anim")

    def user_input(
        self,
        dt: float,
        mouse_click: tuple[bool, bool, bool],
        mouse_pos: tuple[int, int],
    ):
        self.pellet_delay += dt
        if self.pellet_delay >= self.max_delay:
            self.pellet_delay = self.max_delay

        if mouse_click[0] and self.pellet_delay >= self.max_delay:
            Pellet(
                self.pellet_group,
                self.player.rect.center,
                self.pellet_img,
                mouse_pos,
            )
            self.pellet_delay = 0

    def collision(self):
        for pellet in self.pellet_group:
            for maraca in self.maraca_group:
                if maraca.rect.colliderect(pellet.rect):
                    PelletExplode(
                        pellet, self.hit_explosion_group, pellet.pos, self.pellet_frames
                    )
            for bull in self.bull_group:
                if pg.sprite.collide_mask(bull, self.player):
                    print("hit")
                if bull.rect.colliderect(pellet.rect):
                    PelletExplode(
                        pellet, self.hit_explosion_group, pellet.pos, self.pellet_frames
                    )
                    bull.hit()

    def update(
        self,
        dt: float,
        keys: pg.key.get_pressed,
        mouse_pos: tuple[int, int],
        events: pg.event.get,
        screen: pg.Surface,
    ):
        for ev in events:
            if ev.type == self.ATTACK_EVENT:
                attack_type = random.randint(0, 1)
                match attack_type:
                    case 0:
                        Bull(self.bull_group, self.bull_frames)
                    case 1:
                        pass

        # Background Update
        self.background.movement(dt)
        self.background.animate_sky(dt)
        self.background.draw_sky(screen)
        self.background.draw_wrapped(screen, 0, 2)
        self.background.draw_wrapped(screen, 1, 1)
        self.background.draw_wrapped(screen, 2, 4)

        # Maraca Update
        sorted_maracas = sorted(self.maraca_group.sprites(), key=lambda m: m.pos.z)
        for maraca in sorted_maracas:
            maraca.animate(dt)
            maraca.movement(dt)
            maraca.draw(screen)

        # Player Update
        self.player.animate(dt)
        self.player.movement(dt, keys)
        self.player.draw(screen)

        # Wand Update
        self.wand.rotate(mouse_pos)
        self.wand.update_pos(self.player.rect.center)
        self.wand.draw(screen)

        # Train Update
        self.train.movement(dt)
        self.train.draw(screen)

        # Bull Update
        for bull in self.bull_group:
            bull.animate(dt)
            bull.draw(screen)
            if bull.update(dt):
                bull.kill()

        # Pellet Update
        for pellet in self.pellet_group:
            pellet.rotate(dt)
            pellet.movement(dt)
            pellet.draw(screen)
        for expl in self.hit_explosion_group:
            expl.animate(dt)
            expl.draw(screen)
