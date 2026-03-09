from assets import Assets

class Entity:
    def __init__(self, game, width, height):
        self.game = game
        self.dead = False
        self.width = width
        self.height = height
        self.frames = []
        self.frame = 0
        self.anim_timer = 0
        self.anim_next = ""

    def update(self):
        pass

    def draw(self):
        pass

    def set_animation(self, name, next=""):
        self.frames = Assets.animations[f"lemming_{name}"]
        self.anim_next = next