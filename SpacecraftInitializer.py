from spacecraft.wheel.Wheel import TorqueModeWheel
from spacecraft.satellite.Satellite import CubeSat, ComplexSat
from data.DatasetGenerator import DatasetGenerator


def init():
    satellite = None

    use_sample = input("Use sample Spacecraft? (y/n): ")
    if use_sample == "y":
        satellite = get_sample_satellite()
    elif use_sample == "n":
        satellite = construct_spacecraft()

    DatasetGenerator(satellite, 1000).generate(save=True)

    return satellite


def get_sample_satellite():
    wheel = TorqueModeWheel(9.5, 0.347, 7300, 0.17)
    satellite = CubeSat(wheel, 500, 1)

    return satellite

def construct_spacecraft():
    print("Constructing wheel...")
    wheel_specs = [float(spec) for spec in input("Enter wheel specs like this: *mass;radius;max_speed;max_torque*: ").split(";")]
    print(wheel_specs)
    wheel = TorqueModeWheel(*wheel_specs)

    print("Constructing satellite...")
    satellite_class = CubeSat if input("Choose satellite type (1 - CubeSat, 2 - ComplexSat): ") == "1" else ComplexSat
    satellite = object.__new__(satellite_class)

    satellite_specs = [float(spec) for spec in input("Enter satellite specs like this: *mass;length* for CubeSat and *inertia* for ComplexSat: ").split(";")]
    satellite.__init__(wheel, *satellite_specs)

    return satellite
