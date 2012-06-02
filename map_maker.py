import pyglet
import tile
import menu
import serial
import sys

IMAGES = {"save" : pyglet.image.load("resources/art/menu_save.png"),
          "load" : pyglet.image.load("resources/art/menu_load.png"),
          "new" : pyglet.image.load("resources/art/menu_new.png")}

class Console(object):
    def __init__(self):
        self.output = pyglet.text.Label("")
        self.input = pyglet.text.Label("")
    def draw(self):
        self.output.draw()
        self.input.draw()
    def readline(self, text = None):
        if text: return raw_input(text)
        else: return raw_input()
        return read_text
    def write(self, text):
        self.output.text += "\n" + text

new_io = Console()
    

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
        serial.save_file(f_working, obj_working)
    def load_file(self):
        try:
            reply = raw_input("What file would you like to load? ")
            self.obj_working = serial.load_file(reply)
        except IOError:
            print "File not found."
    def new_file(self):
        self.obj_working = tile.Map(10, 10)
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
