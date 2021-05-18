import pandas as pd

from data.Sample import Sample
from simulation.Simulation import InstructedSimulation
from utils import Utils
from utils.DatasetConstants import *


class DatasetGenerator:
    def __init__(self, satellite, size):
        self.size = size
        self.satellite = satellite
        self.samples = []
        self.dt = 0.5

    def generate(self, save=True):
        print("Dataset generation. Please wait...")
        for i in range(0, self.size):
            u = Utils.get_random_rounded(MIN_OUTPUT, MAX_OUTPUT)
            self.__generate_sample(u)

        for i in range(0, round(self.size * 0.05)):
            u = 0.1 ** i
            self.__generate_sample(u)

        if save:
            self.save_data()

    def __generate_sample(self, u):
        simulation = InstructedSimulation(self.satellite, self.dt, u)
        simulation.run()

        dw = self.satellite.speed / self.dt

        self.samples.append(Sample(dw, u))

        self.satellite.reset()

    def save_data(self):
        df = pd.DataFrame(columns=DATASET_COLUMNS)

        for sample in self.samples:
            df = df.append(sample.to_dataframe(), ignore_index=True)

        df.to_csv('data.csv', index=False)
