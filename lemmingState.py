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
            lem.setAnimation("splat")
            lem.frame = 0
            lem.dead = True
            return
        
        lem.falling = 0

        lem.setAnimation("walk")

        if not lem.isOnFloor():
            lem.setState(Faller)
            return

        height = lem.floorHeightInFront()
        if height <= lem.climbheight:
            lem.x += lem.direction
            # rise up to new ground level
            lem.y -= height
        else:
            lem.direction *= -1

        if lem.isNear(lem.game.level.end_position, 15):
            lem.game.points += 1
            lem.dead = True
            # Remove now
            lem.frame = -1

class Faller(LemmingState):
    def update(self):
        lem = self.lem

        if lem.isOnFloor():
            lem.setState(Walker)
            return

        lem.y += 1

        lem.falling += 1
        if lem.falling > 3:
            lem.setAnimation("fall")