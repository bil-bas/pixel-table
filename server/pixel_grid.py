from __future__ import absolute_import, division, print_function, unicode_literals

from collections import OrderedDict
import math
import sys

from termcolor import cprint
import numpy as np

from .pixel import Pixel
from .pixel_controller import PixelController


class PixelGrid(object):
    WIDTH, HEIGHT = 16, 16

    def __init__(self):
        super(PixelGrid, self).__init__()
        self.data = np.zeros([self.WIDTH, self.HEIGHT, 3])
        self._cell_width = None

        self._pixels = OrderedDict()
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                self._pixels[x, y] = Pixel(x, y, pixel_grid=self)

        self._pixel_controller = PixelController()
        self._pixel_controller.open()

        self._pixel_held = None

    @property
    def pixels(self):
        return self._pixels.values()

    def clear(self, color=(0, 0, 0)):
        for pixel in self.pixels:
            pixel.color = color

    def pixel(self, x, y):
        return self._pixels[x, y]

    def export_data(self):
        return self.data.copy()

    def import_data(self, data):
        self.data = data

    def pixel_at(self, position):
        x = min(max(math.floor(position[0] / self._cell_width), 0), self.WIDTH - 1)
        y = self.HEIGHT - min(max(math.floor(position[1] / self._cell_width), 0), self.HEIGHT - 1) - 1
        return self._pixels[x, y]

    def get_color(self, x, y):
        return self.data[x][y]

    def set_color(self, x, y, color):
        self.data[x][y] = color

    def fade(self, amount):
        for pixel in self.pixels:
            r, g, b = pixel.color
            pixel.color = max(r - amount, 0), max(g - amount, 0), max(b - amount, 0)

    def update(self, dt):
        self._pixel_controller.write_pixels(self.data)

    def dump(self):
        print("===       Apotable %2dx%2d       ===" % (self.data.shape[0], self.data.shape[1]))
        print("+" + "-" * (self.data.shape[0] * 2) + "+", file=sys.stderr)

        for y in range(self.data.shape[1]):
            print("|", end="")

            for x in range(self.data.shape[0]):
                r, g, b = self.data[x][y]
                if r >= 0.5 and g <= 0.2 and b <= 0.2:
                    color = "red"
                elif r <= 0.2 and g >= 0.5 and b <= 0.2:
                    color = "green"
                elif r <= 0.2 and g <= 0.2 and b >= 0.5:
                    color = "blue"
                elif r >= 0.5 and g >= 0.5 and b >= 0.5:
                    color = "white"
                elif r >= 0.25 and g >= 0.25 and b >= 0.25:
                    color = "grey"
                else:
                    color = None

                cprint("  ", on_color="on_" + color if color else None, attrs=[], end="")

            print("|")
        print("+" + "-" * (self.data.shape[0] * 2) + "+", file=sys.stderr)



