import math
import physics


class Gravity(physics.Controller):
    def __init__(self, gravity=-9.8):
        physics.Controller.__init__(self)
        self._gravity = gravity

    def update(self, time):
        distance = 0.5 * self._gravity * math.pow(time, 2)
        self.parent.move(0, -distance)


class Jump(physics.Controller):
    def __init__(self, jumpAmount=10):
        physics.Controller.__init__(self)
        self._jumpAmount = jumpAmount

    def update(self, time):
        self.parent.move(0, -self._jumpAmount)

