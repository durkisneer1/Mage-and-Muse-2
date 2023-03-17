import enum


class AttackType(enum.Enum):
    BULL = enum.auto()
    TACO = enum.auto()


class Images(enum.Enum):
    bull_frames = "./res/bull"
    taco_img = "./res/taco/taco.png"
    pellet_img = "./res/weapon/projectile/Projectile.png"
    pellet_frames = "./res/weapon/projectile/anim"
    window_img = "./res/interface/pause_window.png"
