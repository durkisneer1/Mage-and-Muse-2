import pygame as pg
import random

from src.constants import *
from src.support import import_folder
from src.decor import Background, Train, TrainFire
from src.enums import AttackType, Images
from src.player import Player, Wand
from src.maraca import Maraca
from src.bull import Bull
from src.pellet import Pellet, PelletExplode
from src.skull import Skull
from src.taco import Taco
from src.UI import HealthBar, PlayerHealth
from src.rain import Rain


class Gameplay:
    def __init__(self):
        # Level Setup Setup
        self.player = Player()
        self.wand = Wand()
        self.background = Background()
        self.train = Train()

        # Fire Setup
        ground_fire_frames = import_folder(Images.ground_fire_frames, scale=1.5)
        self.fire_group = pg.sprite.Group()
        for i in (20, 95, 175, 240):
            random_frame = random.randint(0, len(ground_fire_frames) - 1)
            TrainFire(self.fire_group, ground_fire_frames, i, random_frame)

        # Darken Screen
        self.tint_surf = pg.Surface(WIN_SIZE, pg.SRCALPHA)
        self.tint_surf.fill((0, 0, 0, 135))

        # Rain Setup
        self.rain_group = pg.sprite.Group()
        self.rain_images = import_folder(Images.rain_drop_images)
        self.RAIN_EVENT = pg.event.custom_type()
        pg.time.set_timer(self.RAIN_EVENT, 50)

        # Maraca Setup
        self.boss_group = pg.sprite.Group()
        maraca_left = Maraca(self.boss_group, True)
        maraca_right = Maraca(self.boss_group, False)

        # Skull Setup
        flower_frames = import_folder(Images.flower_frames)
        fire_eye_frames = import_folder(Images.fire_eye_frames, scale=1.5)
        Skull(self.boss_group, Images.idle_skull_img, flower_frames, 15, 3)
        self.active_skull = Skull(
            None, Images.active_skull_img, fire_eye_frames, 12, 20
        )

        # Bull Attack Setup
        self.ATTACK_EVENT = pg.event.custom_type()
        pg.time.set_timer(self.ATTACK_EVENT, 2000)
        self.attack_group = pg.sprite.Group()
        self.bull_frames = import_folder(Images.bull_frames)
        self.taco_img = pg.image.load(Images.taco_img).convert_alpha()

        # Pellet Setup
        self.max_delay = 2.5
        self.pellet_delay = self.max_delay
        self.hit_explosion_group = pg.sprite.Group()
        self.pellet_group = pg.sprite.Group()
        self.pellet_img = pg.image.load(Images.pellet_img).convert()
        self.pellet_frames = import_folder(Images.pellet_frames)

        self.UI_group = pg.sprite.Group()
        HealthBar(self.UI_group, (0, 0), "left", maraca_left)  # Maraca Health
        HealthBar(self.UI_group, (WIN_WIDTH, 0), "right", maraca_right)  # Maraca Health
        PlayerHealth(self.UI_group, self.player)  # Player Health

    def user_input(
        self,
        events: list[pg.event.Event],
        mouse_click: tuple[bool, bool, bool],
        mouse_pos: tuple[int, int],
        dt: float,
        *args,
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

        for ev in events:
            if ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE:
                return "pause"

        if self.player.health <= 0:
            return "exit"

    def adjust_ui(self, target_obj: any):
        target_obj.health -= 1
        for UI in self.UI_group:
            if target_obj.health <= 0 and hasattr(target_obj, "kill"):
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
                    self.adjust_ui(boss)
        for attack in self.attack_group:
            if (
                attack.hitbox.colliderect(self.player.rect)
                and not self.player.on_cooldown
                and not self.player.dashed
            ):
                self.player.hit()
                self.adjust_ui(self.player)
            for pellet in self.pellet_group:
                if attack.rect.colliderect(pellet.rect):
                    PelletExplode(
                        pellet,
                        self.hit_explosion_group,
                        pellet.pos.copy(),
                        self.pellet_frames,
                    )
                    attack.hit()

    def queue_attacks(self, events: pg.event.get):
        for ev in events:
            if ev.type == self.ATTACK_EVENT and len(self.boss_group) > 1:
                attack_type = random.choice(list(AttackType))
                if attack_type == AttackType.BULL:
                    Bull(self.attack_group, self.bull_frames)
                elif attack_type == AttackType.TACO:
                    Taco(self.attack_group, self.taco_img)
            elif ev.type == self.RAIN_EVENT and not bool(self.boss_group):
                for i in range(15):
                    Rain(self.rain_group, self.rain_images)

    def update(
        self,
        screen: pg.Surface,
        keys: pg.key.get_pressed,
        mouse_pos: tuple[int, int],
        events: pg.event.get,
        dt: float,
    ):
        self.collision()
        self.queue_attacks(events)

        # Background Update
        self.background.update(dt)
        self.background.draw(screen, bool(self.boss_group))

        # Maraca/Skull Update
        if g := self.boss_group:
            sorted_bosses = sorted(self.boss_group.sprites(), key=lambda m: m.pos.z)
            for boss in sorted_bosses:
                boss.update(dt)
                boss.draw(screen)
                if len(g) == 1:
                    boss.kill()
        else:
            screen.blit(self.tint_surf, (0, 0))

            # Active Skull Update
            self.active_skull.update(dt)
            self.active_skull.draw(screen)

            # Train Fire Update
            for fire in self.fire_group:
                fire.update(dt)
                fire.draw(screen)

            # Rain Update
            for rain in self.rain_group:
                rain.update(dt)
                rain.draw(screen)

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
