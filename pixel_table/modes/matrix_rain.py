import random
import math

from kivy.properties import BoundedNumericProperty, ObjectProperty

from .mode import Mode


class Drop:
    def __init__(self):
        self._x = self._y = self._length = self._speed = 0
        self.reset()

    def update(self, dt):
        self._y -= self._speed * dt

        if self._y < - self._length - 5:
            self.reset()

    def reset(self, initial=True):
        self._x = random.randrange(0, 16)
        self._y = random.randrange(15, 35 if initial else 20)
        self._length = random.randrange(5, 12)
        self._speed = random.randrange(4, 7)

    def tail(self):
        head_y = math.floor(self._y)

        for i, y in enumerate(range(head_y, head_y + self._length)):
            r = b = (max(2 - i, 0)) * 0.25

            if 0 <= y <= 15:
                yield self._x, y, (r, 0.5, b)


class MatrixRain(Mode):
    NAME = "Matrix Rain"

    num_drops = ObjectProperty(None)
    _drops = []

    def on_activated(self):
        self.grid.clear()
        for i in range(int(self.num_drops.value)):
            self.add_drop()

    def add_drop(self):
        self._drops.append(Drop())

    def on_deactivated(self):
        self._drops.clear()

    def update_num_drops(self, value):
        value = int(value)
        for i in range(len(self._drops), value):
            self.add_drop()
        self._drops = self._drops[:value]

    def update(self, dt):
        if dt > 0.2:  # Ignore long initial dt.
            return

        # Fade all.
        for pixel in self.grid.children:
            color = pixel.color
            pixel.color = (0, color[1] - (0.2 * dt), 0)

        # Move drops down a bit & restart any that have fallen off..
        for drop in self._drops:
            drop.update(dt)

            for x, y, color in drop.tail():
                pixel = self.grid.pixel(x, y)
                pixel.color = color
