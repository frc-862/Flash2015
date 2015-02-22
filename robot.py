import wpilib
from subsystem.drivetrain import DriveTrain
from handlers.autonomous import AutonHandler
from threading import Timer
from subsystem.lifter import Lifter

TEST_BENCH = False  # Whether we're using the test chassis


class FlashRobot(wpilib.IterativeRobot):

    def robotInit(self):
        """
        Used as a constructor
        """
        self.drivetrain = DriveTrain(self, testBench=TEST_BENCH)
        self.drivetrain.zero()

        if not TEST_BENCH:
            self.lifter = Lifter(self)

        self.autonHandler = AutonHandler(self)

        self.mainDriverStick = wpilib.Joystick(0)
        self.copilotStick = wpilib.Joystick(1)

        self.wasTurning = False

    def autonomousInit(self):
        self.autonHandler.start()
        self.drivetrain.drive.drive(-1, 0.0)
        wpilib.Timer.delay(2.0)
        self.drivetrain.drive.drive(0, 0)

    def teleopInit(self):
        self.autonHandler.end()

    def log(self):
        self.drivetrain.log()

    def autonomousPeriodic(self):
        self.log()

    def teleopPeriodic(self):
        self.operatorControl()
        self.log()

    def operatorControl(self):
        """Runs the motors with arcade steering."""

        self.drivetrain.drive.setSafetyEnabled(True)

        while self.isOperatorControl() and self.isEnabled():
            # Float value, between -1 and 1, representing a forced turn amount. Used for gyro.
            forcedTurn = None

            if abs(self.mainDriverStick.getZ()) > 0.05:  # We're turning, 0.05 is a deadzone
                self.wasTurning = True
            else:
                angle = self.drivetrain.gyro.getAngle()
                angleDiff = (angle + 180) % 360 - 180  # How far the angle is from 0 TODO verify my math
                if abs(angleDiff) > 10:  # TODO check if 10 is a good deadzone
                    kp = 0.03  # Proportional constant for how much to turn based on angle offset
                    forcedTurn = -angle*kp
                else:
                    forcedTurn = None  # They were in the deadzone, and gyro is center, so force no turn at all

            if abs(self.mainDriverStick.getZ()) < 0.05 and self.wasTurning:  # We were turning, now we've stopped
                self.wasTurning = False

                Timer(0.75, lambda: self.drivetrain.gyro.reset()).start()  # Zero the gyro in 0.75 seconds. Need to tune the time.

            if forcedTurn is not None:
                self.drivetrain.arcadeDrive(self.mainDriverStick, rotateAxis=2, invertTurn=True, rotateValue=forcedTurn)  # 2 is horizontal on the right stick
            else:
                self.drivetrain.arcadeDrive(self.mainDriverStick, invertTurn=True, rotateAxis=2)  # 2 is horizontal on the right stick

            if not TEST_BENCH:
                self.drivetrain.arcadeStrafe(self.mainDriverStick)

            if not TEST_BENCH:
                self.lifter.arcadeDrive(self.copilotStick)

            wpilib.Timer.delay(.005)  # give time for the motor to update

if __name__ == "__main__":
    import codecs
    import sys
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    wpilib.run(FlashRobot)
