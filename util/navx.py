# Special thanks to team 4009 for their NavX python code as an example

import serial
import threading

_FLOAT_LENGTH_RUNES = 7
_NAVX_YPRC_MSG_BEGIN = "!y"


class NavX:

    def __init__(self):
        self.dataThread = _NavXDataThread(lambda: self.zero())
        self.dataThread.start()

        self.zeroPitch = 0
        self.zeroYaw = 0
        self.zeroRoll = 0

    def getYaw(self):
        with self.dataThread.mutex:
            return (self.getRawYaw() - self.zeroYaw) % 360

    def getPitch(self):
        with self.dataThread.mutex:
            return (self.getRawPitch() - self.zeroPitch) % 360

    def getRoll(self):
        with self.dataThread.mutex:
            return (self.getRawRoll() - self.zeroRoll) % 360

    def getRawYaw(self):
        with self.dataThread.mutex:
            return self.dataThread.yaw + 180

    def getRawPitch(self):
        with self.dataThread.mutex:
            return self.dataThread.pitch + 180

    def getRawRoll(self):
        with self.dataThread.mutex:
            return self.dataThread.roll + 180

    def zero(self):
        self.zeroPitch = self.getRawPitch()
        self.zeroYaw = self.getRawYaw()
        self.zeroRoll = self.getRawRoll()


class _NavXDataThread(threading.Thread):

    def __init__(self, onFirstNumbers):
        super().__init__(name="NavX Data Listener", daemon=True)
        self.mutex = threading.RLock()

        self.serial = serial.Serial(1, 57500)

        self.yaw = 0.0
        self.pitch = 0.0
        self.roll = 0.0

        self.onFirstNumbers = onFirstNumbers
        self.firstNumbers = True

    def _update(self, dataString):
        if dataString.startswith(_NAVX_YPRC_MSG_BEGIN):
            dataStringNumbers = dataString[len(_NAVX_YPRC_MSG_BEGIN):-2]  # -2 is the length of the checksum at the end

            try:
                self.yaw = float(dataStringNumbers[:-_FLOAT_LENGTH_RUNES*3])
                self.pitch = float(dataStringNumbers[_FLOAT_LENGTH_RUNES:-_FLOAT_LENGTH_RUNES*2])
                self.roll = float(dataStringNumbers[_FLOAT_LENGTH_RUNES*2:-_FLOAT_LENGTH_RUNES])
                self.compassHeading = float(dataStringNumbers[_FLOAT_LENGTH_RUNES*3:])
                if self.firstNumbers:
                    self.onFirstNumbers()
                    self.firstNumbers = False
            except Exception:
                print("Failed to parse NavX string: %s" % dataString)

    def run(self):
        while True:
            try:
                line = self.serial.readline().decode("utf8")
                self._update(line)
            except(UnicodeDecodeError):
                pass
