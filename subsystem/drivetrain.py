import wpilib
from wpilib.command import Subsystem
import hal
from util.navx import NavX
from pinout import *


RAMP_AMOUNT = 0.006
RAMP_DOWN_AMOUNT = 0.02


class DriveTrain(Subsystem):

    def __init__(self, robot, testBench=False):
        super().__init__()
        self.robot = robot

        self.isTestbench = testBench

        if testBench:
            self.rightMainDriveMotor1 = wpilib.Talon(8)
            self.rightMainDriveMotor2 = wpilib.Talon(9)

            self.leftMainDriveMotor1 = wpilib.Talon(0)
            self.leftMainDriveMotor2 = wpilib.Talon(1)

            self.drive = wpilib.RobotDrive(frontLeftMotor=self.leftMainDriveMotor1, rearLeftMotor=self.leftMainDriveMotor2,
                                           frontRightMotor=self.rightMainDriveMotor1, rearRightMotor=self.rightMainDriveMotor2)

            wpilib.LiveWindow.addActuator("Drive Train", "Right Main Motor 1", self.rightMainDriveMotor1)
            wpilib.LiveWindow.addActuator("Drive Train", "Right Main Motor 2", self.rightMainDriveMotor2)
            wpilib.LiveWindow.addActuator("Drive Train", "Left Main Motor 1", self.leftMainDriveMotor1)
            wpilib.LiveWindow.addActuator("Drive Train", "Left Main Motor 2", self.leftMainDriveMotor2)
        else:
            self.rightMainDriveMotor = wpilib.VictorSP(RIGHT_MAIN_DRIVE)
            self.leftMainDriveMotor = wpilib.VictorSP(LEFT_MAIN_DRIVE)

            self.frontTDrive = wpilib.VictorSP(FRONT_STRAFE)
            self.backTDrive = wpilib.VictorSP(BACK_STRAFE)

            self.drive = wpilib.RobotDrive(self.leftMainDriveMotor, self.rightMainDriveMotor)
            self._strafeDrive = wpilib.RobotDrive(self.frontTDrive, self.backTDrive)

            wpilib.LiveWindow.addActuator("Drive Train", "Right Main Motor", self.rightMainDriveMotor)
            wpilib.LiveWindow.addActuator("Drive Train", "Left Main Motor", self.leftMainDriveMotor)

            wpilib.LiveWindow.addActuator("Drive Train", "Front Strafe", self.frontTDrive)
            wpilib.LiveWindow.addActuator("Drive Train", "Back Strafe", self.backTDrive)

        if not testBench:
            try:
                self.navX = NavX()
            except Exception as ex:
                print("Failed to setup NavX: %s" % ex)
                self.navX = None
        else:
            self.navX = None

        self.driveSpeedMult = 0.5
        self.lastMoveValue = 0
        self.lastStrafeValue = 0

        wpilib.LiveWindow.addActuator("Drive Train", "Gyro", self.navX)

    def log(self):
        if self.navX is not None:
            wpilib.SmartDashboard.putNumber("Gyro Yaw", self.navX.getRawYaw())

    def zero(self):
        """Resets the encoders and gyro"""
        if self.navX is not None:
            self.navX.zero()

    def arcadeStrafe(self, stick):
        if not self.isTestbench:
            self.setStrafe(stick.getX())

    def setStrafe(self, amount):
        """Sets the strafe motors. USE THIS, NOT THE strafeDrive DIRECTLY!!! YOU CAN RUN THE MOTORS AGAINST EACHOTHER!"""
        # TODO confirm that this won't drive them against each other. Keep in mind that it's simulating the front one as a left motor and back one as a right motor (or the other way around, but you get the point)
        # Making one of them negative is to reverse the default behavior of inverting one side

        amount = self._getRampValue(self.lastStrafeValue, amount, RAMP_AMOUNT, RAMP_DOWN_AMOUNT)
        self.lastStrafeValue = amount

        self._strafeDrive.setLeftRightMotorOutputs(amount*self.driveSpeedMult, -amount*self.driveSpeedMult)

    def arcadeDrive(self, stick,
                    moveStick=None, rotateStick=None,
                    moveAxis=None, rotateAxis=None,
                    moveValue=None, rotateValue=None,
                    squaredInputs=True,
                    invertMove=False, invertTurn=False):
        """Drive the robot using the arcade controller

        :param stick: The joystick to use for Arcade single-stick driving.
            The Y-axis will be selected for forwards/backwards and the
            X-axis will be selected for rotation rate.
        :param moveStick: The Joystick object that represents the
            forward/backward direction.
        :param moveAxis: The axis on the moveStick object to use for
            forwards/backwards (typically Y_AXIS).
        :param rotateStick: The Joystick object that represents the rotation
            value.
        :param rotateAxis: The axis on the rotation object to use for the
            rotate right/left (typically X_AXIS).
        :param moveValue: The value to use for forwards/backwards.
        :param rotateValue: The value to use for the rotate right/left.
        :param squaredInputs: Setting this parameter to True decreases the
            sensitivity at lower speeds.  Defaults to True if unspecified.
        """

        if moveStick is None:
            moveStick = stick

        if moveValue is None:
            if moveAxis is None:
                moveValue = moveStick.getY()
            else:
                moveValue = moveStick.getRawAxis(moveAxis)

        if rotateStick is None:
            rotateStick = stick

        if rotateValue is None:
            if rotateAxis is None:
                rotateValue = rotateStick.getX()
            else:
                rotateValue = rotateStick.getRawAxis(rotateAxis)

        if invertMove:
            moveValue = -moveValue
        if invertTurn:
            rotateValue = -rotateValue

        # local variables to hold the computed PWM values for the motors
        if not self.drive.kArcadeStandard_Reported:
            hal.HALReport(hal.HALUsageReporting.kResourceType_RobotDrive,
                          self.drive.getNumMotors(),
                          hal.HALUsageReporting.kRobotDrive_ArcadeStandard)
            self.drive.kArcadeStandard_Reported = True

        moveValue = self.drive.limit(moveValue)
        rotateValue = self.drive.limit(rotateValue)

        moveValue = self._getRampValue(self.lastMoveValue, moveValue, RAMP_AMOUNT, RAMP_DOWN_AMOUNT)

        self.lastMoveValue = moveValue

        if squaredInputs:
            # square the inputs (while preserving the sign) to increase fine
            # control while permitting full power
            if moveValue >= 0.0:
                moveValue = (moveValue * moveValue)
            else:
                moveValue = -(moveValue * moveValue)
            if rotateValue >= 0.0:
                rotateValue = (rotateValue * rotateValue)
            else:
                rotateValue = -(rotateValue * rotateValue)

        if moveValue > 0.0:
            if rotateValue > 0.0:
                leftMotorSpeed = moveValue - rotateValue
                rightMotorSpeed = max(moveValue, rotateValue)
            else:
                leftMotorSpeed = max(moveValue, -rotateValue)
                rightMotorSpeed = moveValue + rotateValue
        else:
            if rotateValue > 0.0:
                leftMotorSpeed = -max(-moveValue, rotateValue)
                rightMotorSpeed = moveValue + rotateValue
            else:
                leftMotorSpeed = moveValue - rotateValue
                rightMotorSpeed = -max(-moveValue, -rotateValue)

        self.drive.setLeftRightMotorOutputs(leftMotorSpeed*self.driveSpeedMult, rightMotorSpeed*self.driveSpeedMult)

    @staticmethod
    def _getRampValue(lastValue, desiredValue, rampAmount, downAmount=None):
        if 0 >= lastValue > desiredValue:
            return lastValue - rampAmount
        elif 0 <= lastValue < desiredValue:
            return lastValue + rampAmount

        if downAmount:
            if desiredValue < lastValue:
                return lastValue - downAmount
            elif desiredValue > lastValue:
                return lastValue + downAmount

        if desiredValue < 0 < lastValue or desiredValue > 0 > lastValue:
            return 0

        return desiredValue
