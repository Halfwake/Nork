import pyglet
import menu

IMAGES = {}
IMAGES["toolbar"] = pyglet.image.load("resources/art/toolbar.png")

class Toolbar(object):
    def __init__(self):
        self.menu_frame = MenuFrame()
        self.mode = self.menu_frame
    def on_draw(self):
        self.mode.on_draw()
    def on_mouse_press(self, x, y, symbol, modifiers):
        self.mode.on_mouse_press(x, y, symbol, modifiers)
        
class MenuFrame(object):
    def on_draw(self):
        pass
    def on_mouse_press(self, x, y, symbol, modifiers):
        pass



        
def ask_user(talk_choice):
    toolbar_instance.mode = talk_choice
    return
        
