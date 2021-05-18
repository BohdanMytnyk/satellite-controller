import pandas as pd

from utils import DatasetConstants


class Sample:
    def __init__(self, dw, u):
        self.dw = dw
        self.u = u

    def __repr__(self):
        return "{0};{1};\n".format(self.dw, self.u)

    def to_dataframe(self):
        return pd.DataFrame(data = [[self.dw, self.u]],
                            columns=DatasetConstants.DATASET_COLUMNS)
