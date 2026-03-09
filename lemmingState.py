class LemmingState:
    def __init__(self, lemming):
        self.lem = lemming

    def update(self):
        pass

class Walker(LemmingState):
    def update(self):
        lem = self.lem
        level = lem.game.level

        if lem.falling > level.max_height_to_die:
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
        if height <= lem.climbheight:
            lem.x += lem.direction
            # rise up to new ground level
            lem.y -= height
        else:
            lem.direction *= -1

        if lem.is_near(lem.game.level.end_position, 15):
            lem.game.points += 1
            lem.dead = True
            # Remove now
            lem.frame = -1

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

        lem.y += delta
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

        lem.y += 1

        #lem.falling += 1
        #if lem.falling > 3:
        #    lem.set_animation("fall")

class Stoper(LemmingState):
    def update(self):
        pass

LemmingState.states = {
    "Parado": Stoper,
    "Andando": Walker,
    "Caindo": Faller,
    "Flutuando": Floater
}
