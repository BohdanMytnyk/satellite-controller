from controller.ModelTrainer import ModelTrainer
from utils import MessageResources, Utils
from utils.Constants import OUTPUT_MIN_BOUND, OUTPUT_MAX_BOUND
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

from utils.Utils import get_power_in_bounds


class Controller:
    def __init__(self, desired_speed):
        self.output = 0
        self.desired_speed = desired_speed

        self.last_time = 0
        self.last_desired_speed = 0
        self.last_error = 0
        self.last_output = 0

    def __repr__(self):
        return "<controller>"

    def control(self, speed, t):
        raise Exception(MessageResources.METHOD_NOT_IMPLEMENTED)

    def reset(self):
        self.last_time = 0


class CustomPIDController(Controller):
    def __init__(self, desired_speed, Kp, Ki, Kd):
        super().__init__(desired_speed)
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.S = 0

    def control(self, speed, t):
        dt = t - self.last_time

        if dt < 0.5:
            return self.output

        error = self.desired_speed - speed

        # Calculating I component
        if self.Ki > 0.0:
            self.S = Utils.get_value_in_bounds(self.S + self.Ki * error * dt, OUTPUT_MIN_BOUND, OUTPUT_MAX_BOUND)

        # Calculating D component
        d_error = (self.desired_speed - self.last_desired_speed) / dt - (error - self.last_error) / dt

        # Calculating output
        new_output = self.Kp * error + self.S + self.Kd * d_error
        self.output = Utils.get_value_in_bounds(new_output, OUTPUT_MIN_BOUND, OUTPUT_MAX_BOUND)

        # Remember for the next steps
        self.last_output = self.output
        self.last_time = t
        self.last_error = error
        self.last_desired_speed = self.desired_speed

        return self.output

    def __repr__(self):
        return "CustomPIDController()"


class MLController(Controller):
    def __init__(self, desired_speed):
        super().__init__(desired_speed)
        self.ml_model = ModelTrainer(self._get_model_instance()).get_trained_model()

    def control(self, speed, t):
        dt = t - self.last_time

        if dt < 0.5:
            return self.output

        error = (self.desired_speed - speed)
        scaled_speed = error / dt
        to_predict = np.array([[scaled_speed]])

        self.last_time = t
        self.output = get_power_in_bounds(self.ml_model.predict(to_predict))
        return self.output

    def _get_model_instance(self):
        raise NotImplementedError

    def __repr__(self):
        return str(self._get_model_instance())


class RegressionTreeController(MLController):
    def __init__(self, desired_speed):
        super().__init__(desired_speed)

    def _get_model_instance(self):
        return DecisionTreeRegressor()


class RandomForestController(MLController):
    def __init__(self, desired_speed):
        super().__init__(desired_speed)

    def _get_model_instance(self):
        return RandomForestRegressor()

class LinearRegressionController(MLController):
    def __init__(self, desired_speed):
        super().__init__(desired_speed)

    def _get_model_instance(self):
        return LinearRegression()

class GradientBoostingController(MLController):
    def __init__(self, desired_speed):
        super().__init__(desired_speed)

    def _get_model_instance(self):
        return GradientBoostingRegressor()
