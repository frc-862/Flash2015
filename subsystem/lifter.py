from wpilib.command import Subsystem
import wpilib


class Lifter(Subsystem):

    def __init__(self, robot):
        super().__init__()

        self.robot = robot

        self.leftLiftMotor = wpilib.VictorSP(6)
        self.rightLiftMotor = wpilib.VictorSP(3)

        self._liftDrive = wpilib.RobotDrive(self.leftLiftMotor, self.rightLiftMotor)

    def setMotors(self, power):
        # negative is to keep the motors moving in the same direction TODO VERIFY WHETHER OR NOT THEY NEED TO BE IN THE SAME DIRECTION!!!!!
        self._liftDrive.setLeftRightMotorOutputs(power, -power)

    def arcadeDrive(self, joystick):
        self.setMotors(joystick.getY())
