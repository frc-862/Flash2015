import wpilib
from wpilib.buttons import JoystickButton
import util.logitech_controller as ctrlmap
import commands.drivercommands as dcmds


class OI:

    """
    Operator interface of the robot.
    Manages commands to run based on driver input.
    """

    def __init__(self, robot):
        self.robot = robot

        self.driver_joystick = wpilib.Joystick(0)
        self.copilot_joystick = wpilib.Joystick(1)

        self.driver_a_button = JoystickButton(self.driver_joystick, ctrlmap.BUTTON_A)
        self.driver_b_button = JoystickButton(self.driver_joystick, ctrlmap.BUTTON_B)

        self.driver_a_button.whenPressed(dcmds.SetDriveSpeedMult(robot, 1))
        self.driver_b_button.whenPressed(dcmds.SetDriveSpeedMult(robot, 0.5))
