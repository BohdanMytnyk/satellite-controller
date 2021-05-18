import ControllerInitializer
import SpacecraftInitializer
from simulation.Simulation import ControlledSimulation
from matplotlib import pyplot as plt

desired_speed = float(input("Enter desired speed: "))
simulation_duration = float(input("Enter simulation duration: "))

satellite = SpacecraftInitializer.init()
chosen_controllers = ControllerInitializer.init(desired_speed)

for controller in chosen_controllers:
    simulation = ControlledSimulation(satellite, simulation_duration, controller)
    tw_values = simulation.run()
    plt.plot(*tw_values)

plt.legend([str(controller) for controller in chosen_controllers])
plt.show()