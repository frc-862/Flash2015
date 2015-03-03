from wpilib.command import CommandGroup, Command
from commands.lifter_cmds import *


class RunAuton(CommandGroup):

    def __init__(self, robot):
        super().__init__()
        self.addSequential(CloseArms(robot))
        self.addSequential(DriveDistance(robot, -1))
        self.addSequential(StrafeDistance(robot, -1))
        self.addSequential(LiftHeight(robot, 1))
        self.addSequential(DriveDistance(robot, 1))
        self.addSequential(OpenArms(robot))
        self.addSequential(LiftHeight(robot, -1))
        self.addSequential(CloseArms(robot))
        self.addSequential(DriveDistance(robot, -1))
        self.addSequential(StrafeDistance(robot, -1))
        self.addSequential(LiftHeight(robot, 2))
        self.addSequential(DriveDistance(robot, 1))
        self.addSequential(OpenArms(robot))
        self.addSequential(LiftHeight(robot, -2))
        self.addSequential(CloseArms(robot))


class DriveDistance(Command):

    def __init__(self, robot, distance):
        super().__init__()
        self.requires(robot.drivetrain)
        self.distance = distance
        self.robot = robot

    def initialize(self):
        pass

    def execute(self):
        pass

    def isFinished(self):
        return True

    def end(self):
        pass

    def interrupted(self):
        pass


class StrafeDistance(Command):

    def __init__(self, robot, distance):
        super().__init__()
        self.requires(robot.drivetrain)
        self.distance = distance
        self.robot = robot

    def initialize(self):
        pass

    def execute(self):
        pass

    def isFinished(self):
        return True

    def end(self):
        pass

    def interrupted(self):
        pass


class TurnAngle(Command):

    def __init__(self, robot, degrees, deadzone):
        super().__init__()
        self.requires(robot.drivetrain)
        self.target = degrees
        self.robot = robot
        self.startAngle = 0
        self.deadzone = deadzone

    def initialize(self):
        self.startAngle = self.robot.drivetrain.navX.getRawYaw()
        self.target = self.startAngle + self.target

    def execute(self):
        # TODO use PID
        self.robot.drivetrain.drive(1, 1 if self.target > 0 else -1)

    def isFinished(self):
        return abs(self.robot.drivetrain.navX.getRawYaw - self.target) < self.deadzone

    def end(self):
        self.robot.drivetrain.navX.zero()

    def interrupted(self):
        self.robot.drivetrain.navX.zero()