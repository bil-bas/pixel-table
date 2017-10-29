import math
from collections import OrderedDict

import numpy as np
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

from server.pixel_controller import PixelController
from .pixel import Pixel


class PixelGrid(Widget):
    WIDTH, HEIGHT = 16, 16

    data = ObjectProperty(np.zeros([WIDTH, HEIGHT, 3]), force_dispatch=True)

    def __init__(self, **kwargs):
        super(PixelGrid, self).__init__(**kwargs)

        self._cell_width = None

        self._pixels = OrderedDict()
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                self._pixels[x, y] = Pixel(x, y, pixel_grid=self)

        self._pixel_controller = PixelController()
        self._pixel_controller.open()

        self.bind(size=self.update_canvas)

        self.register_event_type("on_pixel_down")
        self.register_event_type("on_pixel_move")
        self.register_event_type("on_pixel_up")
        self.register_event_type("on_pixel_held")

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
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        self._cell_width = self.width / self.WIDTH
        draw_size = (self._cell_width - 1, self._cell_width - 1)

        with self.canvas:
            for (x, y), pixel in self._pixels.items():
                pixel.color_on_canvas = Color(*pixel.color, mode='rgb')
                Rectangle(pos=(self.x + x * self._cell_width, self.y + (self.HEIGHT - y - 1) * self._cell_width),
                          size=draw_size)

    def pixel_at(self, position):
        x = min(max(math.floor(position[0] / self._cell_width), 0), self.WIDTH - 1)
        y = self.HEIGHT - min(max(math.floor(position[1] / self._cell_width), 0), self.HEIGHT - 1) - 1
        return self._pixels[x, y]

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            pixel = self.pixel_at(touch.pos)
            self._pixel_held = pixel
            self.dispatch("on_pixel_down", pixel)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            pixel = self.pixel_at(touch.pos)
            self._pixel_held = pixel
            self.dispatch("on_pixel_move", pixel)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self._pixel_held = None
            self.dispatch("on_pixel_up", self.pixel_at(touch.pos))

    def on_pixel_down(self, pixel):
        pass

    def on_pixel_move(self, pixel):
        pass

    def on_pixel_up(self, pixel):
        pass

    def on_pixel_held(self, pixel, dt):
        pass

    def get_color(self, x, y):
        return self.data[x][y]

    def set_color(self, x, y, color):
        self.data[x][y] = color

    def fade(self, amount):
        for pixel in self.pixels:
            r, g, b = pixel.color
            pixel.color = max(r - amount, 0), max(g - amount, 0), max(b - amount, 0)

    def update(self, dt):
        if self._pixel_held is not None:
            self.dispatch("on_pixel_held", self._pixel_held, dt)

        self._pixel_controller.write_pixels(self.data)