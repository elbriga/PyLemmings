class LemmingState:
    def __init__(self, lemming):
        self.lem = lemming

    def update(self):
        pass

class Walker(LemmingState):
    def update(self):
        lem = self.lem
        level = lem.game.level

        lem.setAnimation("walk")

        bottomleft = level.groundatposition((lem.x - lem.width / 2, lem.y + 1))
        bottomright = level.groundatposition((lem.x + lem.width / 2, lem.y + 1))
        if not bottomleft and not bottomright:
            lem.state = Faller(lem)
            return

        height = 0
        found = False
        # find the height of the ground in front of a lemming
        # up to the maximum height a lemming can climb
        while not found and height <= lem.climbheight:
            # the pixel 'in front' of a lemming will depend on
            # the direction it's traveling
            if lem.direction == 1:
                positioninfront = (lem.x + lem.width / 2, lem.y - height)
            else:
                positioninfront = (lem.x - lem.width / 2, lem.y - height)

            if not level.groundatposition(positioninfront):
                lem.x += lem.direction
                # rise up to new ground level
                lem.y -= height
                found = True

            height += 1

        # turn the lemming around if the ground in front
        # is too high to climb
        if not found:
            lem.direction *= -1
        
        if lem.isNear(lem.game.level.end_position, 15):
            lem.game.points += 1
            lem.dead = True
            # Remove now
            lem.frame = -1

class Faller(LemmingState):
    def update(self):
        lem = self.lem
        level = lem.game.level

        bottomleft = level.groundatposition((lem.x - lem.width / 2, lem.y + 1))
        bottomright = level.groundatposition((lem.x + lem.width / 2, lem.y + 1))
        if bottomleft or bottomright:
            lem.state = Walker(lem)
            return

        lem.y += 1

        lem.falling += 1
        if lem.falling > 3:
            lem.setAnimation("fall")