from wpilib.command import Command


class OpenArms(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot


class CloseArms(Command):

    def __init__(self, robot):
        super().__init__()
        self.robot = robot


class LiftHeight(Command):

    def __init__(self, robot, height):
        super().__init__()
        self.robot = robot
        self.height = height