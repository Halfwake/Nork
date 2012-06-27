import pyglet
import tile
import menu
import serial
import sys
from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename



IMAGES = {"save" : pyglet.image.load("resources/art/menu_save.png"),
          "load" : pyglet.image.load("resources/art/menu_load.png"),
          "new" : pyglet.image.load("resources/art/menu_new.png")}

class Interface(pyglet.window.Window):
    def __init__(self):
        super(Interface, self).__init__()
        self.new_file()
        self.camera = tile.Camera(self.obj_working, 10, 10, 0, 0)
        self.fps_display = pyglet.clock.ClockDisplay(color = (200.0, 200.0, 200.5, 128.0))
        pyglet.clock.set_fps_limit(40)
        self.save_button = menu.Button(0, 0, IMAGES["save"], self.save_file)
        self.load_button = menu.Button(self.save_button.x + self.save_button.width, 0, IMAGES["load"], self.load_file)
        self.new_button = menu.Button(self.load_button.x + self.load_button.width, 0, IMAGES["new"], self.new_file)
    def save_file(self):
        self.f_working = asksaveasfilename()
        serial.save_file(self.f_working, self.obj_working)
    def load_file(self):
        try:
            self.f_working = askopenfilename()
            self.obj_working = serial.load_file(self.f_working)
        except IOError:
            print "File not found."
    def new_file(self):
        self.obj_working = tile.Map(100, 100)
    def on_mouse_press(self, x, y, symbol, modifiers):
        self.save_button.click(x, y)
        self.load_button.click(x, y)
        self.new_button.click(x, y)
    def on_draw(self):
        self.clear()
        self.camera.draw()
        self.save_button.draw()
        self.load_button.draw()
        self.new_button.draw()
        self.fps_display.draw()
root = Interface()
pyglet.app.run()
