import math

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd


class ModelTrainer:
    def __init__(self, model):
        self.model = model

    def get_trained_model(self):
        data = pd.read_csv('data.csv', delimiter=",")

        train_x, test_x, train_y, test_y = train_test_split(data.iloc[:, :-1], data.iloc[:, [-1]],
                                                            test_size=0.3)

        self.model.fit(train_x, train_y.values.ravel())

        pred_y = self.model.predict(test_x)

        self.print_metrics(metrics.mean_squared_error(test_y, pred_y), self.model.score(test_x, test_y))

        return self.model

    def print_metrics(self, mse, r2):
        print("#############################")
        print(str(self.model) + " metrics:")
        print("MSE = " + str(mse))
        print("R^2 = " + str(r2))
        print("#############################")
