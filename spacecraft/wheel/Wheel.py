from utils import MessageResources
import math

from utils.Constants import T_MAX_TORQUE, DEFAULT_K_P, SAMPLE_TIME
from utils.Utils import get_value_in_bounds, get_power_in_bounds


class Wheel:
    def __init__(self, mass, radius, max_speed, max_torque):
        self.mass = mass
        self.radius = radius

        self.speed = 0
        self.max_speed = max_speed * 2 * math.pi / 60  # Convert speed from RPM to rad/s
        self.desired_speed = 0

        self.torque = 0
        self.max_torque = max_torque
        self.desired_torque = 0

        self.inertia = 0.5 * mass * (radius ** 2)

        self.t = 0

    def activate_mode(self, power):
        raise Exception(MessageResources.METHOD_NOT_IMPLEMENTED)

    def control(self, dt):
        raise Exception(MessageResources.METHOD_NOT_IMPLEMENTED)

    def update(self, dt):
        self.control(dt)

        a = self.torque / self.inertia
        self.speed += get_value_in_bounds(a * dt, -self.max_speed, self.max_speed)

    def reset(self):
        self.torque = 0
        self.desired_torque = 0
        self.speed = 0
        self.desired_speed = 0

    def get_angular_momentum(self):
        return self.speed * self.inertia


class TorqueModeWheel(Wheel):
    def activate_mode(self, power):
        self.desired_torque = get_power_in_bounds(power) * self.max_torque

    def control(self, dt):
        if self.desired_torque > self.torque:
            self.torque += self.max_torque * dt / T_MAX_TORQUE
        elif self.desired_torque < self.torque:
            self.torque -= self.max_torque * dt / T_MAX_TORQUE

        self.torque = get_value_in_bounds(self.torque, -self.max_torque, self.max_torque)

