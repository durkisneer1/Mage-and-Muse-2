import enum


class AttackType(enum.Enum):
    BULL = enum.auto()
    TACO = enum.auto()


class Images:
    bull_frames = "./res/bull"
    taco_img = "./res/taco/taco.png"
    cheese_img = "./res/taco/cheese.png"
    pellet_img = "./res/weapon/projectile/Projectile.png"
    pellet_frames = "./res/weapon/projectile/anim"
    window_img = "./res/interface/pause_window.png"
    ground_fire_frames = "./res/fire/ground"
    fire_eye_frames = "./res/fire/eye"
    idle_skull_img = "./res/skull/idle.png"
    active_skull_img = "./res/skull/active.png"
    flower_frames = "./res/skull/flower"
    fireball_img = "./res/skull/fireball/fireball.png"
