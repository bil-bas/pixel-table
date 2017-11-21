from __future__ import absolute_import, division, print_function, unicode_literals

import logging

import numpy as np


class MockNeoPixel(object):
    def __init__(self, num, pin, freq_hz=800000, dma=5, invert=False,
                 brightness=255, channel=0, strip_type=0):
        self._num = num

    def begin(self):
        pass

    def setPixelColorRGB(self, index, r, g, b):
        assert 0 <= index < self._num
        assert 0 <= r <= 255, r
        assert 0 <= g <= 255, g
        assert 0 <= b <= 255, b

    def show(self):
        pass

try:
    from neopixel import Adafruit_NeoPixel as NeoPixel
except ImportError:
    NeoPixel = MockNeoPixel

_logger = logging.getLogger(__name__)

# NeoPixels
LED_COUNT = 256  # Number of LED pixels.
LED_PIN = 21  # GPIO pin connected to the pixels (must support PWM!). 18=PWM, 21=PCM, 10=SPI-MOSI
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5  # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)


class NeoPixels(object):
    def __init__(self):
        self._pixels = self._open()

    def _open(self):
        pixels = NeoPixel(num=LED_COUNT, pin=LED_PIN, freq_hz=LED_FREQ_HZ, dma=LED_DMA, invert=LED_INVERT,
                          brightness=LED_BRIGHTNESS)
        try:
            pixels.begin()
        except RuntimeError:
            print("Failed to initialize to NeoPixel")
            pixels = MockNeoPixel(num=LED_COUNT, pin=LED_PIN)

        for i in range(LED_COUNT):
            pixels.setPixelColorRGB(i, 0, 0, 0)
        pixels.show()
        return pixels

    def write_pixels(self, data):
        for y, row in enumerate((data * 255).astype(np.uint8)):
            for x, color in enumerate(row):
                self._pixels.setPixelColorRGB(y * 16 + x, *color)
        self._pixels.show()
