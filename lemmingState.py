class LemmingState:
    def __init__(self, lemming):
        self.lem = lemming

    def update(self):
        pass

class Walker(LemmingState):
    def update(self):
        lem = self.lem

        if lem.falling > lem.game.minHeightToDie:
            # Die!
            lem.set_animation("splat")
            lem.frame = 0
            lem.dead = True
            return
        lem.falling = 0

        lem.set_animation("walk")

        if not lem.is_on_floor():
            lem.set_state("Caindo")
            return

        height = lem.floor_height_in_front()
        if height > lem.climbHeight:
            lem.direction *= -1
            return
        
        # Andar
        lem.rect.x += lem.direction
        # Subir o terreno se preciso
        lem.rect.y -= height

class Faller(LemmingState):
    def update(self):
        lem = self.lem

        if lem.is_on_floor():
            lem.set_state("Andando")
            return


        if lem.falling > 100:
            delta = 4
        elif lem.falling > 50:
            delta = 3
        else:
            delta = 2

        lem.rect.y += delta
        lem.falling += delta

        if lem.falling > 100:
            if lem.hasUmbrella:
                lem.set_state("Flutuando")
                lem.set_animation("open", "float")
        elif lem.falling > 10:
            lem.set_animation("fall")

class Floater(LemmingState):
    def update(self):
        lem = self.lem

        if lem.is_on_floor():
            lem.set_state("Andando")
            return

        lem.rect.y += 1

class Blocker(LemmingState):
    def update(self):
        pass

LemmingState.states = {
    "Parado": Blocker,
    "Andando": Walker,
    "Caindo": Faller,
    "Flutuando": Floater
}
