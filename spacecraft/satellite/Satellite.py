class Satellite:
    def __init__(self, wheel):
        self.wheel = wheel

        self.speed = 0
        self.inertia = 0
        self.t = 0

    def update(self, dt):
        self.t += dt
        angular_momentum = self.wheel.get_angular_momentum()
        self.speed = angular_momentum / self.inertia  # w = L / I
        self.wheel.update(dt)

    def reset(self):
        self.speed = 0
        self.t = 0
        self.wheel.reset()


class CubeSat(Satellite):
    def __init__(self, wheel, mass, length):
        super().__init__(wheel)
        self.inertia = (mass / 6) * (length ** 2)


class ComplexSat(Satellite):
    def __init__(self, wheel, inertia):
        super().__init__(wheel)
        self.inertia = inertia
