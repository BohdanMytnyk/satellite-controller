from utils.Constants import POWER_MIN_BOUND, POWER_MAX_BOUND
import random


def get_value_in_bounds(value, min_value, max_value):
    if value < min_value:
        return min_value
    elif value > max_value:
        return max_value
    return value


def get_power_in_bounds(power):
    return get_value_in_bounds(power, POWER_MIN_BOUND, POWER_MAX_BOUND)


def get_random_rounded(min_value, max_value):
    return round(random.uniform(min_value, max_value), 3)
