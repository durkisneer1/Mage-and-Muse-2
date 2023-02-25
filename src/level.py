import pygame as pg
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
        self.proj_delay = 3
        self.hit_explosion_group = pg.sprite.Group()
        self.pellet_group = pg.sprite.Group()
        self.proj_img = pg.image.load("../res/misc/projectile/Projectile.png").convert()
        self.proj_frames = import_folder("../res/misc/projectile/anim")

    def user_input(self, dt, mouse_click, mouse_pos):
        if self.proj_delay >= 3:
            self.proj_delay = 3
        else:
            self.proj_delay += dt

        if mouse_click[0] and self.proj_delay >= 3:
            Pellet(
                self.pellet_group,
                self.player.rect.center,
                self.proj_img,
                mouse_pos,
            )
            self.proj_delay = 0

    def collision(self):
        for maraca in self.maraca_group:
            for proj in self.pellet_group:
                if maraca.rect.colliderect(proj.rect):
                    PelletExplode(self.hit_explosion_group, proj.pos, self.proj_frames)
                    proj.kill()

        for bull in self.bull_group:
            if pg.sprite.collide_mask(bull, self.player):
                print("hit")
            for proj in self.pellet_group:
                if bull.rect.colliderect(proj.rect):
                    PelletExplode(self.hit_explosion_group, proj.pos, self.proj_frames)
                    proj.kill()
                    bull.hit()

    def update(self, dt, keys, mouse_pos, events, screen):
        for ev in events:
            if ev.type == self.ATTACK_EVENT:
                Bull(self.bull_group, self.bull_frames)

        # Background Update
        self.background.movement(dt)
        self.background.animate_sky(dt)
        self.background.draw_sky(screen)
        self.background.draw_wrapped(screen, 0, 2)
        self.background.draw_wrapped(screen, 1, 1)
        self.background.draw_wrapped(screen, 2, 4)

        # Maraca Update
        for mar in self.maraca_group:
            mar.animate(dt)
            mar.movement(dt)
            mar.draw(screen)

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
            if bull.bound(dt):
                bull.kill()

        # Pellet Update
        for proj in self.pellet_group:
            proj.rotate(dt)
            proj.movement(dt)
            proj.draw(screen)
        for expl in self.hit_explosion_group:
            expl.animate(dt)
            expl.draw(screen)
