import math

from utils import MessageResources, Constants
import numpy as np
import time


class Simulation:
    def __init__(self, satellite, duration):
        self.satellite = satellite
        self.duration = duration

    def run(self):
        raise Exception(MessageResources.METHOD_NOT_IMPLEMENTED)


class ControlledSimulation(Simulation):
    def __init__(self, satellite, duration, controller):
        super().__init__(satellite, duration)
        self.controller = controller

    def run(self):
        w_values = []
        t_values = []

        for t in np.arange(0, self.duration, Constants.DT):
            output = self.controller.control(self.satellite.speed, t)
            self.satellite.wheel.activate_mode(output)
            self.satellite.update(Constants.DT)

            w_values.append(self.satellite.speed)
            t_values.append(t)
        self.satellite.reset()
        return [t_values, w_values]


class InstructedSimulation(Simulation):
    def __init__(self, satellite, duration, constant_output):
        super().__init__(satellite, duration)
        self.constant_output = constant_output

    def run(self):
        for _ in np.arange(0, self.duration, Constants.DT):
            self.satellite.wheel.activate_mode(self.constant_output)
            self.satellite.update(Constants.DT)
