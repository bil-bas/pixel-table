from __future__ import absolute_import, division, print_function, unicode_literals

import glob
from time import sleep
import logging

from serial import Serial
from serial.serialutil import SerialException


_logger = logging.getLogger(__name__)

READY_CHAR = b'R'
NUM_BUCKETS = 16


class MockSerial(object):
    def write(self, data):
        sleep(0.01)

    def read(self):
        sleep(0.05)
        return b"14fsSffZtAZaz190"

    def setDTR(self, value):
        pass


class Arduino(object):
    DEVICE = "/dev/ttyAMA0"
    SERIAL_SPEED = 9600

    def __init__(self):
        self._serial = self._open()
        self.reset_serial()

    def _open(self):
        _logger.info("Trying to connect to %s" % self.DEVICE)
        try:
            serial = Serial(self.DEVICE, self.SERIAL_SPEED)
            _logger.info("Connected to serial port.")
            return serial
        except SerialException:
            pass

        _logger.warning("Failed to connect to a serial port.")
        return MockSerial()

    def reset_serial(self):
        """Reset Serial connection"""
        self._serial.setDTR(False)
        sleep(0.022)
        self._serial.setDTR(True)

    def read_fft_buckets(self):
        self._serial.write("F")
        return [ord(c) for c in self._serial.read(NUM_BUCKETS)]