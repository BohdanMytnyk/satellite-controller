from controller.Controller import CustomPIDController, RegressionTreeController, RandomForestController, \
    LinearRegressionController, GradientBoostingController

CONTROLLER_CLASSES = [LinearRegressionController,
                      GradientBoostingController,
                      RegressionTreeController,
                      RandomForestController]

def init(desired_speed):
    for i, c in enumerate(CONTROLLER_CLASSES):
        print(str(i + 1) + ") " + c.__name__)

    chosen_ids = str(input("Choose the algorithms using semicolon (use * for all): ")).split(";")

    chosen_controllers = [object.__new__(controller_class) for i, controller_class in enumerate(CONTROLLER_CLASSES) if
                          str(i) in chosen_ids or '*' in chosen_ids]

    for c in chosen_controllers: c.__init__(desired_speed)

    chosen_controllers.append(CustomPIDController(desired_speed, 500, 0, 20))

    return chosen_controllers