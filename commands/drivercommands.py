from wpilib.command import Command


class SetDriveSpeedMult(Command):

    def __init__(self, robot, multiplier):
        super().__init__()
        self.requires(robot.drivetrain)
        self.multiplier = multiplier
        self.robot = robot

    def initialize(self):
        self.robot.drivetrain.driveSpeedMult = self.multiplier

    def execute(self):
        pass

    def isFinished(self):
        return True

    def end(self):
        pass

    def interrupted(self):
        pass
