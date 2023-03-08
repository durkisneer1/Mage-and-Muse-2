import pygame as pg
import random  # NOQA
from constants import *
from support import import_folder
from decor import Background, Train
from enums import AttackType
from player import Player, Wand
from maraca import Maraca
from bull import Bull
from pellet import Pellet, PelletExplode
from skull import Skull
from taco import Taco
from UI import HealthUI


class Level:
    def __init__(self):
        # Level Setup Setup
        self.player = Player()
        self.wand = Wand()
        self.background = Background()
        self.train = Train()

        # Maraca Setup
        self.boss_group = pg.sprite.Group()
        maraca_1 = Maraca(self.boss_group, True)
        maraca_2 = Maraca(self.boss_group, False)
        Skull(self.boss_group)

        # Bull Attack Setup
        self.ATTACK_EVENT = pg.event.custom_type()
        pg.time.set_timer(self.ATTACK_EVENT, 2000)
        self.attack_group = pg.sprite.Group()
        self.bull_frames = import_folder("../res/bull")
        self.taco_img = pg.image.load("../res/taco/taco.png").convert_alpha()

        # Pellet Setup
        self.max_delay = 2.5
        self.pellet_delay = self.max_delay
        self.hit_explosion_group = pg.sprite.Group()
        self.pellet_group = pg.sprite.Group()
        self.pellet_img = pg.image.load(
            "../res/misc/projectile/Projectile.png"
        ).convert()
        self.pellet_frames = import_folder("../res/misc/projectile/anim")

        self.UI_group = pg.sprite.Group()
        HealthUI(self.UI_group, (0, 0), "left", maraca_1)  # Maraca Health
        HealthUI(self.UI_group, (WIN_WIDTH, 0), "right", maraca_2)  # Maraca Health

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

    def adjust_UI(self, target_obj: any):
        target_obj.health -= 1
        for UI in self.UI_group:
            if target_obj.health <= 0:
                target_obj.kill()
                UI.kill()
                return
            if UI.target == target_obj:
                UI.update(target_obj)

    def collision(self):
        for boss in self.boss_group:
            for pellet in self.pellet_group:
                if boss.rect.colliderect(pellet.rect) and boss.pos.z > 0:
                    PelletExplode(
                        pellet,
                        self.hit_explosion_group,
                        pellet.pos.copy(),
                        self.pellet_frames,
                    )
                    self.adjust_UI(boss)
        for attack in self.attack_group:
            if (
                attack.hitbox.colliderect(self.player.rect)
                and not self.player.on_cooldown
                and not self.player.dashed
            ):
                self.player.hit()
            for pellet in self.pellet_group:
                if attack.rect.colliderect(pellet.rect):
                    PelletExplode(
                        pellet,
                        self.hit_explosion_group,
                        pellet.pos.copy(),
                        self.pellet_frames,
                    )
                    attack.hit()

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
                attack_type = random.choice(list(AttackType))
                if attack_type == AttackType.BULL:
                    Bull(self.attack_group, self.bull_frames)
                elif attack_type == AttackType.TACO:
                    Taco(self.attack_group, self.taco_img)

        # Background Update
        self.background.update(dt)
        self.background.draw(screen)

        # Maraca/Skull Update
        sorted_bosses = sorted(self.boss_group.sprites(), key=lambda m: m.pos.z)
        for boss in sorted_bosses:
            boss.update(dt)
            boss.draw(screen)

        # Player Update
        self.player.update(dt, keys)
        self.player.draw(screen)

        # Wand Update
        self.wand.update(self.player.rect.center, mouse_pos)
        self.wand.draw(screen)

        # Train Update
        self.train.update(dt)
        self.train.draw(screen)

        # Bull Update
        for attack in self.attack_group:
            if attack.update(dt):
                attack.kill()
            attack.draw(screen)

        # Pellet Update
        for pellet in self.pellet_group:
            pellet.update(dt)
            pellet.draw(screen)
        for expl in self.hit_explosion_group:
            expl.update(dt)
            expl.draw(screen)

        for UI in self.UI_group:
            UI.draw(screen)
