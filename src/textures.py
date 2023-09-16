from src.utils import import_folder, import_image


class Textures:
    def __init__(self):
        # Animations
        self.bull_frames = import_folder("./res/bull")
        self.pellet_frames = import_folder("./res/weapon/projectile/anim")
        self.flower_frames = import_folder("./res/skull/flower")
        self.ground_fire_frames = import_folder("./res/fire/ground", scale=1.5)
        self.fire_eye_frames = import_folder("./res/fire/eye", scale=1.5)

        # Images
        self.taco_img = import_image("./res/taco/taco.png")
        self.idle_skull_img = import_image("./res/skull/idle.png")
        self.active_skull_img = import_image("./res/skull/active.png")
        self.fireball_img = import_image("./res/skull/fireball/fireball.png")
        self.train_img = import_image("./res/train/Train.png")
        self.tambourine_img = import_image("./res/tambourine/tambourine.png")
        self.window_img = import_image("./res/interface/pause_window.png", is_alpha=False)
        self.cheese_img = import_image("./res/taco/cheese.png", is_alpha=False)
        self.pellet_img = import_image("./res/weapon/projectile/Projectile.png", is_alpha=False)
