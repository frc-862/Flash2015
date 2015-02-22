# Special thanks to team 4009 for their NavX python code as an example

import serial
import threading


class NavX:

    def __init__(self):
        self.dataThread = _NavXDataThread()
        self.dataThread.start()

    def getYaw(self):
        with self.dataThread.mutex:
            return self.dataThread.yaw

    def getPitch(self):
        with self.dataThread.mutex:
            return self.dataThread.pitch

    def getRoll(self):
        with self.dataThread.mutex:
            return self.dataThread.roll


class _NavXDataThread(threading.Thread):

    def __init__(self):
        super().__init__(name="NavX Data Listener", daemon=True)
        self.mutex = threading.RLock()

        self.serial = serial.Serial(1, 57500)

        self.yaw = 0.0
        self.pitch = 0.0
        self.roll = 0.0

    def _update(self, dataString):
        # TODO implement
        self.yaw = 0
        self.pitch = 0
        self.roll = 0

    def run(self):
        while True:
            try:
                line = self.serial.readline().decode("utf8")
                self._update(line)
                print(line)
            except(UnicodeDecodeError):
                pass
